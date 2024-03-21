# Selenium-based bot by RIN
# This is a script that will run a bot that will automatically study book rooms from https://bookings.ok.ubc.ca/studyrooms/

# import libraries and modules needed
import os
import sys
import time
import getpass
import traceback
import requests
import platform
import subprocess
import datetime as dt

version = "Beta v2.6"
isRunningFromSource = True
isOnMac = False
isOnWindows = False
isOnUBCOWifi = False

# make reusable variables for future use
# area 6 is coms 1st
area = 6
# com 108 = 16
# com 109 = 17
# com 110 = 18
# and so on...
# com 121 = 29
room = 29
roomStr = ""
# used to keep track of the website
website = "null"
# used to keep track of the current url
current_url = "null"
# used to keep track of the index of the time to extend to
extendIndex = 0
# used to verify if it is the first time extending,
# we want to extend the maximum amount of time possible
# just incase the bot is started late and the room was already booked
validateMaximum = False

roomName = "UBCOBookingBot"
info_file = "data.rin"
areaName = ""


def check_for_updates():
    print("Checking for updates...")
    # URL of the raw content of the script on GitHub
    url = "https://raw.githubusercontent.com/rin-williams/UBCOBookingBot/main/bookingbot.py"

    # Send a GET request to the URL
    response = requests.get(url)

    # If the request was successful
    if response.status_code == 200:
        # Get the content of the script on GitHub
        github_script = response.text

        # Open the local script
        with open("bookingbot.py", "r") as file:
            # Get the content of the local script
            local_script = file.read()

        # Compare the content of the local script with the content of the script on GitHub
        if local_script == github_script:
            print("Your script is up to date on " + version)
        else:
            print("Fetching update from GitHub...")
            # Open the local script in write mode
            with open("bookingbot.py", "w") as file:
                # Overwrite the content of the local script with the content of the script on GitHub
                file.write(github_script)
                print("Your script has been updated")

    if not os.path.exists("BookingBotApp.py") and isRunningFromSource == False:
        print("The app version is available, downloading now...")
        # URL of the raw content of the script on GitHub
        url = "https://raw.githubusercontent.com/rin-williams/UBCOBookingBot/main/BookingBotApp.py"
        # Send a GET request to the URL
        response = requests.get(url)
        # If the request was successful
        if response.status_code == 200:
            # Get the content of the script on GitHub
            github_script = response.text

            # Open the local script in write mode
            with open("BookingBotApp.py", "w") as file:
                # Overwrite the content of the local script with the content of the script on GitHub
                file.write(github_script)
            print("BookingBotApp.py downloaded.")
            print("Please run BookingBotApp.py to use the app version of this bot.")
            time.sleep(5)
            sys.exit()


def scriptInput(input):
    global room
    global roomStr
    global area
    global roomName
    global website
    global extendIndex
    global validateMaximum
    global driver
    global areaName
    # ------------------- FRESH -------------------
    if input == "f":
        validateMaximum = True
        print("\n----------------------------------------")
        print(
            "[FRESH MODE] for room "
            + roomName
            + " in room "
            + areaName
            + " "
            + roomStr
            + "."
        )
        website = (
            "https://bookings.ok.ubc.ca/studyrooms/edit_entry.php?year="
            + str(future_date.year)
            + "&month="
            + str(future_date.month)
            + "&day="
            + str(future_date.day)
            + "&area="
            + str(area)
            + "&room="
            + str(room)
            + "&view=month&hour=6&minute=0"
        )
        driver.get(website)
        findName = driver.find_element(By.ID, "name")
        findName.send_keys(roomName)
        findDesc = driver.find_element(By.ID, "description")
        findDesc.send_keys(
            "UBCOBookingBot "
            + version
            + " bot by rin, made with Python + Selenium library."
            + " DO NOT USE THIS BOT FOR MALICIOUS PURPOSES."
        )
        # find appropriate time
        now = dt.datetime.now()
        then = now.replace(minute=30 * (now.minute // 30), second=0, microsecond=0)
        then = then - dt.timedelta(minutes=30)

        to = then + dt.timedelta(minutes=30)

        print("Booking from", then.strftime("%H:%M"), "to", to.strftime("%H:%M"))

        thenToString = str(then.strftime("%H:%M"))
        toToString = to.strftime("%H:%M")

        findStart = driver.find_element(By.ID, "start_seconds")
        selectStart = Select(findStart)
        selectStart.select_by_visible_text(thenToString)

        findEnd = driver.find_element(By.ID, "end_seconds")
        selectEnd = Select(findEnd)
        selectEnd.select_by_index(0)

        findType = driver.find_element(By.ID, "type")
        selectType = Select(findType)
        selectType.select_by_visible_text("Instructional / Workshop")

        findPhone = driver.find_element(By.ID, "f_phone")
        findPhone.send_keys("250-000-0000")

        findEmail = driver.find_element(By.ID, "f_email")
        findEmail.send_keys("bot@student.ubc.ca")

        findSave = driver.find_element(By.NAME, "save_button")
        findSave.click()

        # turn toToString to a datetime object
        now = dt.datetime.now()
        toToStringDT = dt.datetime.strptime(toToString, "%H:%M")
        toToStringDT = toToStringDT.replace(year=now.year, month=now.month, day=now.day)
        # 30 mins in seconds = 1800
        toWait = 1800 - (now - toToStringDT).total_seconds()
        if (
            driver.current_url
            == "https://bookings.ok.ubc.ca/studyrooms/edit_entry_handler.php"
        ):
            print(
                "\nALERT: Someone else had the current session that I tried to book: "
                + thenToString
                + " to "
                + toToString
            )
            print("Current time:", now.strftime("%H:%M:%S"))
            print(
                "Will try again in next possible time:",
                str(toWait // 60) + "m and",
                str(round(toWait) % 60) + "s.",
            )
            # try again when the minute of current time is 30 or 00
            # minimize the terminal
            time.sleep(5)
            script = """
            tell application "Terminal"
                set miniaturized of front window to true
            end tell
            """
            subprocess.run(["osascript", "-e", script])
            time.sleep(toWait - 9)

            # count down the last 9 seconds and use carraige return to overwrite the previous line)
            count = 4
            print("Trying again in t minus", count, end="", flush=True)
            while count >= 0:
                print("\rTrying again in t minus", count, end="", flush=True)
                time.sleep(1)
                count = count - 1
            print("\n")
            scriptInput("f")
        else:
            print("Created room. Proceeding to extend mode...")
            scriptInput("e")

    # ------------------- EXTEND -------------------
    elif input == "e":
        print("\n----------------------------------------")
        print(
            "[EXTEND MODE] for room "
            + roomName
            + " in room "
            + areaName
            + " "
            + roomStr
            + "."
        )
        website = (
            "https://bookings.ok.ubc.ca/studyrooms/index.php?view=day&page_date="
            + str(future_date.year)
            + "-"
            + str(future_date.month)
            + "-"
            + str(future_date.day)
            + "&area="
            + str(area)
            + "&room="
            + str(room)
        )
        driver.get(website)

        findByBotName = driver.find_elements(
            By.XPATH, f"//a[contains(text(), '{roomName}')]"
        )
        indexError = False
        try:
            lastBotNameElement = findByBotName[-1]
        except IndexError:
            print("\nALERT: No room with name: " + roomName + " found.")
            print("Starting a fresh session...")
            indexError = True

        if indexError == False:
            lastBotNameElement.click()
            print("Located room with name: " + roomName)
            findEditEntry = driver.find_element(
                By.XPATH, "//form[@action='edit_entry.php']"
            )
            findEditEntry.click()

            findEnd = driver.find_element(By.ID, "end_seconds")
            selectEnd = Select(findEnd)

            currentTime = dt.datetime.now()

            options = selectEnd.options
            optionAsTime = ""
            for i in range(len(options)):
                option = options[i]
                # get option as time
                now = dt.datetime.now()
                optionAsTime = now.replace(
                    hour=int(option.text[:2]),
                    minute=int(option.text[3:5]),
                    second=0,
                    year=currentTime.year,
                    month=currentTime.month,
                    day=currentTime.day,
                )
                currentTime = dt.datetime.now()
                # if the
                if optionAsTime >= currentTime and i != 0:
                    # select the one before it and save to make sure
                    selectEnd.select_by_index(i - 1)
                    findSave = driver.find_element(By.NAME, "save_button")
                    findSave.click()
                    validateMaximum = True
                    print("Booked the maximum amount of time possible.")
                    print("Now going to [WAIT MODE]")
                    break

            # Wait mode, but we have to select the bot session again
            findByBotName = driver.find_elements(
                By.XPATH, f"//a[contains(text(), '{roomName}')]"
            )

            indexError = False
            try:
                lastBotNameElement = findByBotName[-1]
            except IndexError:
                print("\nALERT: No room with name: " + roomName + " found.")
                print("Starting a fresh session...")
                indexError = True

            if indexError == False:
                lastBotNameElement.click()
                print("Located room with name: " + roomName)

                findEditEntry = driver.find_element(
                    By.XPATH, "//form[@action='edit_entry.php']"
                )
                findEditEntry.click()

                findEnd = driver.find_element(By.ID, "end_seconds")
                selectEnd = Select(findEnd)

                currentTime = dt.datetime.now()

                options = selectEnd.options
                optionAsTime = ""
                for i in range(len(options)):
                    option = options[i]
                    # get option as time
                    now = dt.datetime.now()
                    optionAsTime = now.replace(
                        hour=int(option.text[:2]),
                        minute=int(option.text[3:5]),
                        second=0,
                        year=currentTime.year,
                        month=currentTime.month,
                        day=currentTime.day,
                    )
                    if optionAsTime > currentTime and i != 0:
                        # select the one before it and save to make sure
                        selectEnd.select_by_index(i)
                        extendIndex = i
                        break

                currentTime = dt.datetime.now()
                timeDiff = optionAsTime - currentTime
                timeDiffSec = round(timeDiff.total_seconds())

                print("\n----------------------------------------")
                print(
                    "[WAIT MODE] for room "
                    + roomName
                    + " in room COMS "
                    + roomStr
                    + "."
                )
                print(
                    "\nCurrent time:",
                    currentTime.strftime("%H:%M:%S") + ",",
                    "Waiting for time to be extendable at:",
                    optionAsTime.strftime("%H:%M") + ":00",
                    "\nTime to wait:",
                    str(timeDiffSec // 60) + "m and",
                    str(timeDiffSec % 60)
                    + "s."
                    + " Program will sleep until extendable.",
                )

                before_sleep_url = driver.current_url
                # minimize the terminal
                time.sleep(5)
                script = """
                tell application "Terminal"
                    set miniaturized of front window to true
                end tell
                """
                subprocess.run(["osascript", "-e", script])

                time.sleep(timeDiffSec - 9)

                # count down the last 9 seconds and use carraige return to overwrite the previous line)
                count = 4
                print("Extending in t minus", count, end="", flush=True)
                while count >= 0:
                    print("\rExtending in t minus", count, end="", flush=True)
                    time.sleep(1)
                    count = count - 1
                print("\n")
                # refresh to see if we are on the same page.
                driver.refresh()
                after_sleep_url = driver.current_url

                if before_sleep_url == after_sleep_url:
                    findEnd = driver.find_element(By.ID, "end_seconds")
                    selectEnd = Select(findEnd)
                    selectEnd.select_by_index(extendIndex)
                    findSave = driver.find_element(By.NAME, "save_button")
                    findSave.click()
                    print("Extended room.")
                else:
                    print("FIX ME")
                    print("User was logged out by CWL Inactivity Policy.")
                    print("url before sleep:", before_sleep_url)
                    print("url after sleep:", after_sleep_url)
                    driver.quit()

                if extendIndex == 3:
                    print("You have reached the end of this booking session.")
                    print(
                        "Will automatically goto [FRESH MODE] in 30 mins, program will sleep until then."
                    )
                    before_sleep_url = driver.current_url
                    time.sleep(1800)
                    driver.refresh()
                    after_sleep_url = driver.current_url
                    if before_sleep_url == after_sleep_url:
                        scriptInput("f")
                    else:
                        print("FIX ME")
                        print("User was logged out by CWL Inactivity Policy.")
                        print("url before sleep:", before_sleep_url)
                        print("url after sleep:", after_sleep_url)
                        driver.quit()

                else:
                    print("Will automatically go to [EXTEND MODE] again in 1 minute.")
                    time.sleep(61)
                    scriptInput("e")
            else:
                scriptInput("f")
        else:
            scriptInput("f")
    else:
        print("Quitting...")
        driver.quit()


def checkRoom():
    global room
    global roomStr
    global info_file
    global area
    global areaName
    foundRoomStr = False
    if os.path.exists(info_file):
        with open(info_file, "r") as file:
            for line in file:
                if "com=" in line:
                    areaName = "COM"
                    area = 7
                    foundRoomStr = True
                    roomStr = line.split("=")[1].strip()
                    # if input starts with 1 and is 3 digits long
                    if roomStr[0] == "0" and len(roomStr) == 3:
                        room = int(roomStr) + 7
                        if 12 <= room <= 15:
                            break
                        else:
                            foundRoom = False
                            print("COMS " + roomStr + " is an invalid room.")
                        area = 5
                    elif roomStr[0] == "1" and len(roomStr) == 3:
                        if str(room) == "":
                            foundRoom = False
                            break
                        room = int(roomStr) - 92
                        if 16 <= room <= 29:
                            break
                        else:
                            foundRoomStr = False
                            print("COMS " + roomStr + " is an invalid room.")
                        area = 6
                    elif roomStr[0] == "3" and len(roomStr) == 3:
                        match str(roomStr):
                            case "":
                                foundRoomStr = False
                                break
                            case "312":
                                room = "39"
                                break
                            case "314":
                                room = "40"
                                break
                            case "316":
                                room = "41"
                                break
                            case "318":
                                room = "42"
                                break
                            case _:
                                room = int(roomStr) - 271
                                if 30 <= room <= 38:
                                    break
                                else:
                                    foundRoomStr = False
                                    print("COMS " + roomStr + " is an invalid room.")
                elif "lib=" in line:
                    areaName = "LIB"
                    foundRoomStr = True
                    roomStr = line.split("=")[1].strip()
                    area = 1
                    match roomStr:
                        case "121":
                            room = 2
                            break
                        case "122":
                            room = 1
                            break
                elif "eme1=" in line:
                    areaName = "EME"
                    foundRoomStr = True
                    area = 8
                    roomStr = line.split("=")[1].strip()
                    room = int(roomStr) - 1108
                    break
                elif "eme2=" in line:
                    areaName = "EME"
                    foundRoomStr = True
                    area = 9
                    roomStr = line.split("=")[1].strip()
                    match roomStr:
                        case "1252":
                            room = 43
                            break
                        case "1254":
                            room = 44
                            break
                        case "2242":
                            room = 46
                            break
                        case "2244":
                            room = 48
                            break
                        case "2246":
                            room = 49
                            break
                        case "2248":
                            room = 50
                            break
                        case "2252":
                            room = 51
                            break
                        case "2254":
                            room = 52
                            break
                        case "2257":
                            room = 53
                            break
                        case _:
                            print("EME " + roomStr + " is an invalid room.")
                            break
        if foundRoomStr == False:
            while True:
                room = input("Booking for room ")
                roomStr = str(room)
                # if input starts with 1 and is 3 digits long
                if room[0] == "0" and len(room) == 3:
                    area = 5
                    # for coms 005 to 008
                    # difference is 7, between 12 and 15
                    room = int(room) + 7
                    if 12 <= room <= 15:
                        break
                    else:
                        print("COM " + roomStr + " is an invalid room.")
                elif room[0] == "1" and len(room) == 3:
                    area = 6
                    # for coms 108 to 121
                    # difference is 92, between 16 and 29
                    if str(room) == "":
                        room = "29"
                        break
                    room = int(room) - 92
                    if 16 <= room <= 29:
                        break
                    else:
                        print("COM " + roomStr + " is an invalid room.")
                elif room[0] == "3" and len(room) == 3:
                    area = 7
                    # for coms 301 to 309
                    # difference is 271, between 30 and 38
                    if str(room) == "":
                        room = "29"
                        break
                    elif str(room) == "312":
                        room = "39"
                        break
                    elif str(room) == "314":
                        room = "40"
                        break
                    elif str(room) == "316":
                        room = "41"
                        break
                    elif str(room) == "318":
                        room = "42"
                        break
                    else:
                        room = int(room) - 271
                        if 30 <= room <= 38:
                            break
                        else:
                            print("COM " + roomStr + " is an invalid room.")
                else:
                    print("COM " + roomStr + " is an invalid room.")
            with open(info_file, "a") as file:
                file.write("com=" + str(roomStr) + "\n")


def checkRoomName():
    global roomName
    global info_file
    if os.path.exists(info_file):
        with open(info_file, "r") as file:
            found = False
            for line in file:
                if "roomName=" in line:
                    roomName = line.split("=")[1].strip()
                    found = True
                    break
            if found == False:
                roomName = input(
                    "Enter room name (will default to UBCOBookingBot if null): "
                )
                if roomName == "":
                    roomName = "UBCOBookingBot"
                with open(info_file, "a") as file:
                    file.write("roomName=" + roomName + "\n")
    else:
        print(info_file + " not found. Creating file...")
        roomName = input("Enter room name (will default to UBCOBookingBot if null): ")
        if roomName == "":
            roomName = "UBCOBookingBot"
        with open(info_file, "w") as file:
            file.write("roomName=" + roomName + "\n")


def checkUsername():
    global info_file
    findUsername = driver.find_element(By.ID, "username")
    # Define the path for the username file
    username = ""
    if os.path.exists(info_file):
        with open(info_file, "r") as file:
            found = False
            for line in file:
                if "username=" in line:
                    username = line.split("=")[1].strip()
                    found = True
                    break
            if found == False:
                username = input("Enter username: ")
                with open(info_file, "a") as file:
                    file.write("username=" + username + "\n")
    findUsername.send_keys(username)


def checkPassword():
    global info_file
    findPassword = driver.find_element(By.ID, "password")
    # Define the path for the password file
    password = ""
    if os.path.exists(info_file):
        with open(info_file, "r") as file:
            found = False
            for line in file:
                if "password=" in line:
                    password = line.split("=")[1].strip()
                    found = True
                    break
            if found == False:
                password = getpass.getpass("Enter password: ")
                with open(info_file, "a") as file:
                    file.write("password=" + password + "\n")
    findPassword.send_keys(password)
    findPassword.send_keys(Keys.RETURN)


def check_if_logged_in():
    global info_file
    global driver
    global isOnUBCOWifi
    current_url = driver.current_url
    current_title = driver.title
    if current_title == "CWL Enhanced Security":
        if not isOnUBCOWifi:
            print("User has logged in, DUO Push needed (not on UBCO WiFi)")
        else:
            print("User has logged in, DUO Push not needed (on UBCO WiFi)")
    else:
        print("\nUser credentials incorrect. Please rerun the program.")
        # delete the username and password files
        os.remove(info_file)
        print("Deleted " + info_file + ". Please rerun the program.")
    while current_url != targetWebsite:
        current_url = driver.current_url
        time.sleep(0.5)
    print("2FA successful.\n")


def check_if_is_running_from_source():
    global isRunningFromSource
    if (
        os.path.exists("INFOS.md")
        or os.path.exists("LICENSE.md")
        or os.path.exists("README.md")
    ):
        isRunningFromSource = True
        print("Running from source code, skipping update check...")
    else:
        isRunningFromSource = False
        print("Running from executable, checking for updates...")


def check_if_on_UBCO_wifi():
    global isOnUBCOWifi
    wifi_name = get_connected_wifi_name()
    if wifi_name == "ubcsecure" or wifi_name == "ubcvisitor":
        print("You are connected to UBCO's WiFi.")
        isOnUBCOWifi = True
    elif wifi_name == None:
        print("You are not connected to a WiFi network, exiting...")
        sys.exit()
    else:
        print("You are connected to: " + wifi_name + ", headless mode disabled.")
        time.sleep(3)


def get_connected_wifi_name():
    if isOnMac:
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
    elif isOnWindows:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True,
            text=True,
        )
        lines = result.stdout.split("\n")
        for line in lines:
            if "SSID" in line:
                return line.split(":")[1].strip()
        return None


# Preprocessing --------------------------------------
check_if_is_running_from_source()

# keep computer awake if on mac
if platform.system() == "Darwin":
    isOnMac = True
    check_if_on_UBCO_wifi()
    if not isRunningFromSource:
        print("System detected: macOS")
        # resize terminal window to be bigger

        script = f"""
        tell application "Terminal"
            activate
            set the font size of window 1 to {15}
            set number of rows of window 1 to {20}
            set number of columns of window 1 to {80}
        end tell
        """
        subprocess.run(["osascript", "-e", script])

        if not os.path.exists("UBBuserdata.dat"):
            print("Checking for dependencies...")
            # check to see if selenium library is installed
            if (
                subprocess.run(
                    ["pip3", "show", "selenium"], capture_output=True
                ).returncode
                == 1
            ):
                print("Selenium library not installed. installing now...")
                subprocess.run(["pip3", "install", "selenium"])
            else:
                print("Selenium library detected")
            # check if requests library is installed
            if (
                subprocess.run(
                    ["pip3", "show", "requests"], capture_output=True
                ).returncode
                == 1
            ):
                print("Requests library not installed. installing now...")
                subprocess.run(["pip3", "install", "requests"])
            else:
                print("Requests library detected")
        check_for_updates()
        print("Keeping computer awake via caffeinate...")
        subprocess.Popen(["caffeinate", "-d", "-i", "-u", "-s", "-t", "10800"])
elif platform.system() == "Windows":
    isOnWindows = True
    check_if_on_UBCO_wifi()
    if not isRunningFromSource:
        if not os.path.exists("UBBuserdata.dat"):
            print("System detected: Windows")
            print("Checking for dependencies...")
            # check to see if selenium library is installed
            if (
                subprocess.run(
                    ["pip", "show", "selenium"], capture_output=True
                ).returncode
                == 1
            ):
                print("Selenium library not installed. installing now...")
                subprocess.run(["pip", "install", "selenium"])
            else:
                print("Selenium library detected")
            # check if requests library is installed
            if (
                subprocess.run(
                    ["pip", "show", "requests"], capture_output=True
                ).returncode
                == 1
            ):
                print("Requests library not installed. installing now...")
                subprocess.run(["pip", "install", "requests"])
            else:
                print("Requests library detected")
        check_for_updates()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, NoSuchWindowException

# start the bot --------------------------------------
print("\n\n----------------------------------------")
print("UBCOBookingBot " + version)
print("Do not use this bot for malicious purposes.")
# calculate date 3 weeks from now
future_date = dt.date.today() + dt.timedelta(weeks=3)
print(
    "You are booking 3 weeks in advance for the date: ",
    future_date.year,
    "-",
    future_date.month,
    "-",
    future_date.day,
    "\n",
)

targetWebsite = (
    "https://bookings.ok.ubc.ca/studyrooms/edit_entry.php?"
    + "year="
    + str(future_date.year)
    + "&month="
    + str(future_date.month)
    + "&day="
    + str(future_date.day)
    + "&area="
    + str(area)
    + "&room="
    + str(room)
    + "&view=month&hour=6&minute=0"
)
driver = None
# if UBB.userdata.dat exists, then we can skip this part
if (
    os.path.exists(info_file)
    and not isRunningFromSource
    and (isOnMac or isOnWindows)
    and isOnUBCOWifi
):
    print(info_file + " found. Running in headless mode...\n")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    driver.get(targetWebsite)
else:
    print("Running in normal mode...")
    driver = webdriver.Chrome()
    driver.set_window_size(600, 600)
    driver.get(targetWebsite)

print("Now accessing:", driver.title)

checkRoom()
checkRoomName()
checkUsername()
checkPassword()
check_if_logged_in()

# ask user if they want to start a new session or extend etc
# userInput = input(
#     "\nAre you here start a fresh session or extend? (f: fresh, e: extend, q: quit): "
# )

# no longer need to ask user for input, extend mode is now default
userInput = "e"
if userInput == "f" or userInput == "e" or userInput == "q":
    try:
        scriptInput(userInput)
    except NoSuchWindowException:
        print("Window was closed. Please restart the program.")
    except WebDriverException:
        print(
            "An error has occured, please check in with the developer.",
        )
        # print stack trace
        traceback.print_exc()
else:
    print("Please enter a valid input.")
