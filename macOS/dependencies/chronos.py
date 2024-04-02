import os
import subprocess
import json

info_file = "prometheus_data.json"

username = ""
password = ""
roomName = ""
building = ""
room = ""
date = ""
startTime = ""
endTime = ""
duration = 0


def check_dependencies():
    with open(info_file, "r") as file:
        data = json.load(file)
        if data.get("hasRequiredLibraries", False):
            print("All required libraries are detected.")
        else:
            subprocess.run(["python3", "macOS/dependencies/dependencies.py"])
            data["hasRequiredLibraries"] = True
            with open(info_file, "w") as file:
                json.dump(data, file)


def transmute_info_file():
    global username, password, roomName, building, room, date, startTime, endTime, duration
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
    print("Starting with params: ")
    print(
        f"Username: {username} \n"
        f"Password: {password} \n"
        f"Room Name: {roomName} \n"
        f"Building: {building} \n"
        f"Room: {room} \n"
        f"Date: {date} \n"
        f"Start Time: {startTime} \n"
        f"End Time: {endTime}"
    )


check_dependencies()
transmute_info_file()
