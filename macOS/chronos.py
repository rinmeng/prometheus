import math
import os
import subprocess
import json
from time import sleep

info_file = "prometheus_data.json"

# user variables
username = ""
password = ""
roomName = ""
building = ""
room = ""
date = ""
startTime = ""
endTime = ""
duration = 0
bookTimesSeconds = []
bookTimes = []


# ubco variables
# https://bookings.ok.ubc.ca/studyrooms/edit_entry.php?drag=1&area=6&start_seconds=21600&end_seconds=28800&rooms[]=28&start_date=2024-04-02
url_date = 0
url_start_seconds = 0
url_end_seconds = 0
url_area = 0
url_rooms = 0
rooms_map = {
    "LIB 121 (4 people)": 2,
    "LIB 122 (4)": 1,
    "COM 005 (4 people)": 12,
    "COM 006 (4)": 13,
    "COM 007 (4)": 14,
    "COM 008 (4)": 15,
    "COM 108 (4 people)": 16,
    "COM 109 (4)": 17,
    "COM 110 (10)": 18,
    "COM 111 (10)": 19,
    "COM 112 (6)": 20,
    "COM 113 (4)": 21,
    "COM 114 (6)": 22,
    "COM 115 (4)": 23,
    "COM 116 (6)": 24,
    "COM 117 (6)": 25,
    "COM 118 (6)": 26,
    "COM 119 (6)": 27,
    "COM 120 (6)": 28,
    "COM 121 (10)": 29,
    "COM 301 (4 people)": 30,
    "COM 302 (4)": 31,
    "COM 303 (4)": 32,
    "COM 304 (4)": 33,
    "COM 305 (6)": 34,
    "COM 306 (4)": 35,
    "COM 307 (6)": 36,
    "COM 308 (4)": 37,
    "COM 309 (6)": 38,
    "COM 312 (4)": 39,
    "COM 314 (4)": 40,
    "COM 316 (4)": 41,
    "COM 318 (4)": 42,
    "EME 1162 (10 people)": 54,
    "EME 1163 (6)": 55,
    "EME 1164 (6)": 56,
    "EME 1165 (6)": 57,
    "EME 1166 (6)": 58,
    "EME 1167 (6)": 59,
    "EME 1168 (6)": 60,
    "EME 1252 (10 people)": 43,
    "EME 1254 (8)": 44,
    "EME 2242 (8)": 46,
    "EME 2244 (8)": 48,
    "EME 2246 (8)": 49,
    "EME 2248 (8)": 50,
    "EME 2252 (8)": 51,
    "EME 2254 (8)": 52,
    "EME 2257 (10)": 53,
}
area_map = {
    "Library": 1,
    "Commons: Floor 0": 5,
    "Commons: Floor 1": 6,
    "Commons: Floor 3": 7,
    "EME: Tower 1": 8,
    "EME: Tower 2": 9,
}
targetURLs = []


def transmute_info_file():
    global username, password, roomName, building, room, date, startTime, endTime, duration
    global url_date, url_start_seconds, url_end_seconds, url_area, url_rooms
    with open(info_file, "r") as file:
        data = json.load(file)
    username = data["username"]
    password = data["password"]
    roomName = data["roomName"]
    building = data["building"]
    room = data["room"]
    date = data["date"]
    startTime = data["startTime"]
    endTime = data["endTime"]

    url_area = area_map[building]
    url_rooms = rooms_map[room]

    # calculate time in seconds where start time can have format of
    # "06:00 (6:00 AM)" and end time can have format of "18:00 (6:00 PM)"
    timeStart = startTime.split(" ")[0]
    timeEnd = endTime.split(" ")[0]
    url_start_seconds = (
        int(timeStart.split(":")[0]) * 3600 + int(timeStart.split(":")[1]) * 60
    )
    url_end_seconds = (
        int(timeEnd.split(":")[0]) * 3600 + int(timeEnd.split(":")[1]) * 60
    )
    # calculate duration
    threshold = 3600 * 2

    duration = url_end_seconds - url_start_seconds
    sessions = duration / threshold

    if sessions <= 1.0:
        session_start = url_start_seconds
        session_end = url_end_seconds
        session = [session_start, session_end]
        bookTimesSeconds.append(session)
    elif 1.0 < sessions <= 2.0:
        # there are 2 sessions
        session1 = [url_start_seconds, url_start_seconds + threshold]
        session2 = [url_start_seconds + threshold, url_end_seconds]
        bookTimesSeconds.append(session1)
        bookTimesSeconds.append(session2)
    elif sessions > 2.0:
        # there are 3 sessions
        session1 = [url_start_seconds, url_start_seconds + threshold]
        session2 = [url_start_seconds + threshold, url_start_seconds + (2 * threshold)]
        session3 = [url_start_seconds + (2 * threshold), url_end_seconds]
        bookTimesSeconds.append(session1)
        bookTimesSeconds.append(session2)
        bookTimesSeconds.append(session3)

    # convert bookTimes to actual time
    for i in range(len(bookTimesSeconds)):
        start = bookTimesSeconds[i][0]
        end = bookTimesSeconds[i][1]

        start_hour = math.floor(start / 3600)
        start_minute = math.floor((start % 3600) / 60)
        end_hour = math.floor(end / 3600)
        end_minute = math.floor((end % 3600) / 60)

        start_hour = str(start_hour) if len(str(start_hour)) == 2 else f"0{start_hour}"
        start_minute = (
            str(start_minute) if len(str(start_minute)) == 2 else f"0{start_minute}"
        )
        end_hour = str(end_hour) if len(str(end_hour)) == 2 else f"0{end_hour}"
        end_minute = str(end_minute) if len(str(end_minute)) == 2 else f"0{end_minute}"

        start_time = f"{start_hour}:{start_minute}"
        end_time = f"{end_hour}:{end_minute}"
        bookTimes.append(f"{start_time} - {end_time}")

    # convert date to url format MM-DD -> YYYY-MM-DD
    url_date = f"2024-{date.split('-')[0]}-{date.split('-')[1]}"

    password_censor = "*" * len(password)

    print("Starting with params: ")
    print(
        f"Username: {username} \n"
        f"Password: {password_censor} \n"
        f"Room Name: {roomName} \n"
        f"Building: {building} (url_area: {url_area})\n"
        f"Room: {room} (url_rooms: {url_rooms}) \n"
        f"Date: {date} (url_date: {url_date})\n"
        f"Start Time: {startTime} (url_start_seconds: {url_start_seconds})\n"
        f"End Time: {endTime} (url_start_seconds: {url_end_seconds}) \n"
        f"Duration: {duration / 3600} hours (sessions: {sessions}) \n"
        f"Book Times: {bookTimes}, (bookTimesSeconds: {bookTimesSeconds})"
    )


def set_target_urls():
    for i in range(len(bookTimes)):
        targetURLs.append(
            f"https://bookings.ok.ubc.ca/studyrooms/edit_entry.php?drag=1&area={url_area}&start_seconds={bookTimesSeconds[i][0]}&end_seconds={bookTimesSeconds[i][1]}&rooms[]={url_rooms}&start_date={url_date}"
        )


def check_dependencies():
    with open(info_file, "r") as file:
        data = json.load(file)
        if data.get("hasRequiredLibraries", False):
            print("All required libraries are detected.")
        else:
            subprocess.run(["python3", "dependencies.py"])
            data["hasRequiredLibraries"] = True
            with open(info_file, "w") as file:
                json.dump(data, file)


def get_connected_wifi_name():
    result = subprocess.run(
        ["networksetup", "-getairportnetwork", "en0"],
        capture_output=True,
        text=True,
    )
    lines = result.stdout.split("\n")
    for line in lines:
        if "Current Wi-Fi Network" in line:
            return line.split(":")[1].strip()
    return None


def isOnUBCOWifi():
    wifi_name = get_connected_wifi_name()
    return wifi_name == "ubcsecure" or wifi_name == "ubcvisitor"


check_dependencies()
transmute_info_file()
set_target_urls()

# post-call
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, NoSuchWindowException

driver = ""

if isOnUBCOWifi():
    print("You are on a UBCO WiFi, going headless...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
else:
    driver = webdriver.Chrome()
    driver.set_window_size(600, 600)


# login part
driver.get(targetURLs[0])

print("Logging in...")
findUsername = driver.find_element(By.ID, "username")
findUsername.send_keys(username)
findPassword = driver.find_element(By.ID, "password")
findPassword.send_keys(password)
findPassword.send_keys(Keys.RETURN)

# await until user leaves
url_loginPage = "authentication.ubc.ca"
counter_seconds = 0
while driver.current_url.find(url_loginPage) != -1:
    print("Waiting for user to leave authentication.ubc.ca")
    counter_seconds += 1
    if counter_seconds > 4:
        print("Wrong credentials. Exiting.")
        driver.close()
        sleep(5)
        driver.quit()
        exit(1)
    sleep(1)
print("User has logged in.")

# await until user leaves something similar to "duosecurity.com"
url_duoSecurity = "duosecurity.com"
while driver.current_url.find(url_duoSecurity) != -1:
    print("Waiting for user finish Duo Security")
    sleep(1)
print("User has finished Duo Security.")

# loop through targetURLs
counter = 0
for targetURL in targetURLs:
    driver.get(targetURL)
    print(f"Booking session {counter + 1} at {bookTimes[counter]}")
    findName = driver.find_element(By.ID, "name")
    findName.send_keys(roomName)
    findDesc = driver.find_element(By.ID, "description")
    findDesc.send_keys(
        "UBCOBookingBot "
        + " bot by rin, made with Python + Selenium library."
        + " DO NOT USE THIS BOT FOR MALICIOUS PURPOSES."
    )
    findPhone = driver.find_element(By.ID, "f_phone")
    findPhone.send_keys("250-000-0000")

    findEmail = driver.find_element(By.ID, "f_email")
    findEmail.send_keys("bot@student.ubc.ca")

    findSave = driver.find_element(By.NAME, "save_button")
    findSave.click()

    # await until user leaves the url targetURL
    entry_handler = "https://bookings.ok.ubc.ca/studyrooms/edit_entry_handler.php"
    if driver.current_url == entry_handler:
        new_end_seconds = bookTimesSeconds[counter][1]
        new_start_seconds = bookTimesSeconds[counter][0]
        while driver.current_url == entry_handler:
            h2 = driver.find_element(By.TAG_NAME, "h2")
            li = driver.find_element(By.TAG_NAME, "li")
            print("Booking failed, reason:")
            print(h2.text)
            if "maximum number" in li.text:
                print(li.text)
                break
            elif "more than 3 weeks" in li.text:
                print(li.text)
                break
            else:
                print(li.text)

            print(
                f"Retrying session {counter + 1}, with new time: {new_start_seconds / 3600} - {new_end_seconds / 3600}"
            )

            new_end_seconds -= 1800

            if new_start_seconds == new_end_seconds:
                print("There are no more available time slots. Exiting.")
                break

            new_targetURL = f"https://bookings.ok.ubc.ca/studyrooms/edit_entry.php?drag=1&area={url_area}&start_seconds={new_start_seconds}&end_seconds={new_end_seconds}&rooms[]={url_rooms}&start_date={url_date}"
            driver.get(new_targetURL)

            findName = driver.find_element(By.ID, "name")
            findName.send_keys(roomName)
            findDesc = driver.find_element(By.ID, "description")
            findDesc.send_keys(
                "UBCOBookingBot "
                + " bot by rin, made with Python + Selenium library."
                + " DO NOT USE THIS BOT FOR MALICIOUS PURPOSES."
            )
            findPhone = driver.find_element(By.ID, "f_phone")
            findPhone.send_keys("250-000-0000")

            findEmail = driver.find_element(By.ID, "f_email")
            findEmail.send_keys("bot@student.ubc.ca")

            findSave = driver.find_element(By.NAME, "save_button")
            findSave.click()
    else:
        while driver.current_url == targetURL:
            print(f"Waiting for user to leave {targetURL}")
            sleep(1)

    counter += 1

driver.close()
print("All sessions have been booked.")
# the link looks like this
# https://bookings.ok.ubc.ca/studyrooms/index.php?view=day&page_date=2024-04-21&area=8&room=54
print(
    "Check your bookings via: "
    + f"https://bookings.ok.ubc.ca/studyrooms/index.php?view=day&page_date={url_date}&area={url_area}&room={url_rooms}"
)
sleep(3)
