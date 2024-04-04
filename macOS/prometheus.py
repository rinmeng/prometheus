# prometheus is a GUI, and a messenger for chronos.py

from datetime import datetime, timedelta
import os
import re
import json
import sys
import time
import requests
import platform
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import IntVar

APPVERSION = "v0"
scriptName = "chronos.py"
appName = "prometheus.py"
info_file = "prometheus_data.json"
saved_date = ""
saved_startTime = ""
saved_endTime = ""

root = tk.Tk()
root.title("prometheus " + APPVERSION)
root.geometry("600x600")
root.resizable(False, False)


welcome_message = "Welcome to prometheus " + APPVERSION
username = ""

welcome_message = ttk.Label(root, text=welcome_message)
welcome_message.pack(pady=10)

username_frame = ttk.Frame(root)
username_frame.pack(pady=10)

username_label = ttk.Label(username_frame, text="Username:")
username_label.pack(side="left", padx=(0, 10))
username_entry = ttk.Entry(username_frame)
username_entry.pack(side="left")


password_frame = ttk.Frame(root)
password_frame.pack(pady=10)

password_label = ttk.Label(password_frame, text="Password:")
password_label.pack(side="left", padx=(0, 10))
password_entry = ttk.Entry(password_frame, show="*")
password_entry.pack(side="left")


building_frame = ttk.Frame(root)
building_frame.pack(pady=10)

building = tk.StringVar()

building_label = ttk.Label(building_frame, text="Building:")
building_label.pack(side="left", padx=(0, 10))
building_option = ttk.Combobox(
    building_frame,
    textvariable=building,
    values=[
        "Library",
        "Commons: Floor 0",
        "Commons: Floor 1",
        "Commons: Floor 3",
        "EME: Tower 1",
        "EME: Tower 2",
    ],
    state="readonly",
)
building_option.pack(side="left")

room_frame = ttk.Frame(root)
room_frame.pack(pady=10)

room_label = ttk.Label(room_frame, text="Room:")
room_label.pack(side="left", padx=(0, 10))
room_option = ttk.Combobox(room_frame, state="readonly")
room_option.pack(side="left")

roomName_frame = ttk.Frame(root)
roomName_frame.pack(pady=10)

roomName_label = ttk.Label(roomName_frame, text="Room name:")
roomName_label.pack(side="left", padx=(0, 5))
roomName_label = ttk.Entry(roomName_frame)
roomName_label.pack(side="left")


def update_options(*args):
    room_option.set("")
    if building.get() == "Library":
        options = ["LIB 121 (4 people)", "LIB 122 (4)"]

    elif building.get() == "EME: Tower 1":
        options = [
            "EME 1162 (10 people)",
            "EME 1163 (6)",
            "EME 1164 (6)",
            "EME 1165 (6)",
            "EME 1166 (6)",
            "EME 1167 (6)",
            "EME 1168 (6)",
        ]
    elif building.get() == "EME: Tower 2":
        options = [
            "EME 1252 (10 people)",
            "EME 1254 (8)",
            "EME 2242 (8)",
            "EME 2244 (8)",
            "EME 2246 (8)",
            "EME 2248 (8)",
            "EME 2252 (8)",
            "EME 2254 (8)",
            "EME 2257 (10)",
        ]
    elif building.get() == "Commons: Floor 0":
        options = [
            "COM 005 (4 people)",
            "COM 006 (4)",
            "COM 007 (4)",
            "COM 008 (4)",
        ]
    elif building.get() == "Commons: Floor 1":
        options = [
            "COM 108 (4 people)",
            "COM 109 (4)",
            "COM 110 (10)",
            "COM 111 (10)",
            "COM 112 (6)",
            "COM 113 (4)",
            "COM 114 (6)",
            "COM 115 (4)",
            "COM 116 (6)",
            "COM 117 (6)",
            "COM 118 (6)",
            "COM 119 (6)",
            "COM 120 (6)",
            "COM 121 (10)",
        ]
    elif building.get() == "Commons: Floor 3":
        options = [
            "COM 301 (4 people)",
            "COM 302 (4)",
            "COM 303 (4)",
            "COM 304 (4)",
            "COM 305 (6)",
            "COM 306 (4)",
            "COM 307 (6)",
            "COM 308 (4)",
            "COM 309 (6)",
            "COM 312 (4)",
            "COM 314 (4)",
            "COM 316 (4)",
            "COM 318 (4)",
        ]
    else:
        options = ["not yet implemented"]

    room_option["values"] = options


building.trace_add("write", update_options)

message_var = tk.StringVar()
message_var.set("")
running = False


def run_bot():
    save_info()
    global running
    date_pattern = re.compile(r"^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$")
    prereq = (
        building_option.get() != ""
        and room_option.get() != ""
        and roomName_label.get() != ""
        and username_entry.get() != ""
        and password_entry.get() != ""
        and roomName_label.get() != ""
        and (
            date_entry.get() != ""
            and date_entry.get() != "MM-DD"
            and date_pattern.match(date_entry.get())
        )
        and startTime.get() != ""
        and endTime.get() != ""
    )
    if not running:
        if prereq:
            running = True
            run_button.config(state="disabled")
            stop_button.config(state="normal")
            print("\n\nALERT: Bot started.")
            message_var.set("Running bot...")
            subprocess.Popen(
                [
                    "python3",
                    scriptName,
                ]
            )
            message_var.set(
                "Bot is running in terminal.\nPlease do not close the terminal window."
                + "\nIf you want to stop the bot, click the 'Stop bot' button."
            )
        else:
            message_var.set("Please fill in all the fields.")


def stop_bot():
    global running
    if running:
        message_var.set("Bot stopped.")
        running = False
        run_button.config(state="normal")
        stop_button.config(state="disabled")
        script = f"""
                do shell script "pkill -f {scriptName}"
                tell application "Terminal"
                    set miniaturized of front window to false
                end tell
                """
        subprocess.run(["osascript", "-e", script])
        subprocess.run(["pkill", "-f", "chromedriver"])
        print("ALERT: Bot stopped.")


def show_terminal():
    script = """
        tell application "Terminal"
            set miniaturized of front window to false
        end tell
        """
    subprocess.run(["osascript", "-e", script])


def hide_terminal():
    script = """
        tell application "Terminal"
            set miniaturized of front window to true
        end tell
        """
    subprocess.run(["osascript", "-e", script])


def toggle_terminal():
    global terminal_shown
    if terminal_shown:
        # If terminal is shown, hide it
        show_terminal()
        terminal_button.config(text="Hide Terminal")
    else:
        hide_terminal()
        terminal_button.config(text="Show Terminal")
    terminal_shown = not terminal_shown


def restart_bot():
    stop_bot()
    run_bot()


def save_info():
    hasRequiredLibraries = False
    if os.path.exists(info_file):
        with open(info_file, "r") as file:
            data = json.load(file)
            hasRequiredLibraries = data["hasRequiredLibraries"]
        with open(info_file, "w") as file:
            data = {
                "username": username_entry.get(),
                "password": password_entry.get(),
                "roomName": roomName_label.get(),
                "building": building_option.get(),
                "room": room_option.get(),
                "date": date_entry.get(),
                "startTime": startTime.get(),
                "endTime": endTime.get(),
                "liveMode": liveMode.get(),
                "hasRequiredLibraries": hasRequiredLibraries,
            }
            json.dump(data, file)
    else:
        with open(info_file, "w") as file:
            data = {
                "username": username_entry.get(),
                "password": password_entry.get(),
                "roomName": roomName_label.get(),
                "building": building_option.get(),
                "room": room_option.get(),
                "date": date_entry.get(),
                "startTime": startTime.get(),
                "endTime": endTime.get(),
                "liveMode": liveMode.get(),
            }
            json.dump(data, file)

        message_var.set("Info saved in " + info_file + " file")


def load_info():
    global username
    global welcome_message

    if os.path.exists(info_file):
        with open(info_file, "r") as file:
            data = json.load(file)
            username = data["username"]
            username_entry.insert(0, username)
            password_entry.insert(0, data["password"])
            roomName_label.insert(0, data["roomName"])
            building.set(data["building"])
            room_option.set(data["room"])
            date_entry.insert(0, data["date"])
            startTime.set(data["startTime"])
            endTime.set(data["endTime"])
            liveMode.set(data.get("liveMode", 0))
    toggle_live_mode()


def toggle_live_mode():
    global saved_date
    global saved_startTime
    global saved_endTime

    if liveMode.get() == 1:
        startTime_label.config(state="disabled")
        endTime_label.config(state="disabled")
        # set the date to 3 weeks from today, and disable the date entry
        saved_date = date_entry.get()
        date = datetime.now() + timedelta(weeks=3)
        date_entry.delete(0, "end")
        date_entry.insert(0, date.strftime("%m-%d"))
        date_entry.config(state="disabled")

        # set start time to the time right now and save it, disable it as well
        saved_startTime = startTime.get()
        saved_endTime = endTime.get()
        now = datetime.now()
        # put it same format as the combobox
        start_time = now.strftime("%H:%M") + " (" + now.strftime("%I:%M %p") + ")"

        startTime.set(start_time)
        endTime.set("indefinetely")

    else:
        startTime_label.config(state="readonly")
        endTime_label.config(state="readonly")
        date_entry.config(state="normal")
        # only delete the date if it was set by the live mode
        if saved_date != "":
            date_entry.delete(0, "end")
            date_entry.insert(0, saved_date)
        if saved_startTime != "" and saved_endTime != "":
            startTime.set(saved_startTime)
            endTime.set(saved_endTime)


date_frame = tk.Frame(root)
date_frame.pack(pady=10)

date_label = tk.Label(date_frame, text="Enter a date (MM-DD):")
date_label.pack(side="left", padx=(0, 10))
date_entry = tk.Entry(date_frame)
date_entry.pack(side="left")


startEndTime_frame = ttk.Frame(root)
startEndTime_frame.pack(pady=10)

startTime_frame = ttk.Frame(startEndTime_frame)
startTime_frame.pack(side="left", padx=(0, 10))

endTime = tk.StringVar()
startTime = tk.StringVar()

availableTimes = [
    "06:00 (6:00 AM)",
    "06:30 (6:30 AM)",
    "07:00 (7:00 AM)",
    "07:30 (7:30 AM)",
    "08:00 (8:00 AM)",
    "08:30 (8:30 AM)",
    "09:00 (9:00 AM)",
    "09:30 (9:30 AM)",
    "10:00 (10:00 AM)",
    "10:30 (10:30 AM)",
    "11:00 (11:00 AM)",
    "11:30 (11:30 AM)",
    "12:00 (12:00 PM)",
    "12:30 (12:30 PM)",
    "13:00 (1:00 PM)",
    "13:30 (1:30 PM)",
    "14:00 (2:00 PM)",
    "14:30 (2:30 PM)",
    "15:00 (3:00 PM)",
    "15:30 (3:30 PM)",
    "16:00 (4:00 PM)",
    "16:30 (4:30 PM)",
    "17:00 (5:00 PM)",
    "17:30 (5:30 PM)",
    "18:00 (6:00 PM)",
    "18:30 (6:30 PM)",
    "19:00 (7:00 PM)",
    "19:30 (7:30 PM)",
    "20:00 (8:00 PM)",
    "20:30 (8:30 PM)",
    "21:00 (9:00 PM)",
    "21:30 (9:30 PM)",
    "22:00 (10:00 PM)",
    "22:30 (10:30 PM)",
    "23:00 (11:00 PM)",
    "23:30 (11:30 PM)",
    "* 00:00 (12:00 AM)",
]


def update_end_time(*args):
    if liveMode.get() == 1:
        return
    start_time = startTime.get()
    start_index = availableTimes.index(start_time)
    end_times = availableTimes[start_index + 1 : start_index + 13]
    endTime.set("")
    endTime_label["values"] = end_times


startTime.trace_add("write", update_end_time)

startTime_label = ttk.Label(startTime_frame, text="Start time:")
startTime_label.pack(side="left", padx=(0, 10))
startTime_label = ttk.Combobox(
    startTime_frame,
    textvariable=startTime,
    values=availableTimes,
    state="readonly",
    width=15,
)
startTime_label.pack(side="left")

endTime_frame = ttk.Frame(startEndTime_frame)
endTime_frame.pack(side="left", padx=(0, 10))

endTime_label = ttk.Label(endTime_frame, text="End time:")
endTime_label.pack(side="left", padx=(0, 10))
endTime_label = ttk.Combobox(
    endTime_frame,
    textvariable=endTime,
    state="readonly",
    width=15,
)
endTime_label.pack(side="left")

liveMode_frame = ttk.Frame(root)
liveMode_frame.pack(pady=10)

liveMode = IntVar()
liveMode_checkbox = ttk.Checkbutton(
    liveMode_frame, text="Live Mode", variable=liveMode, command=toggle_live_mode
)
liveMode_checkbox.pack(side="left", padx=(0, 5))

button_frame = ttk.Frame(root)
button_frame.pack(pady=5)

save_button = ttk.Button(button_frame, text="Save Info", command=save_info)
save_button.pack(side="left", padx=(0, 5))

run_button = ttk.Button(button_frame, text="Start Bot", command=run_bot)
run_button.pack(side="left", padx=(0, 5))

stop_button = ttk.Button(
    button_frame, text="Stop Bot", command=stop_bot, state="disabled"
)
stop_button.pack(side="left", padx=(0, 5))

button_frame2 = ttk.Frame(root)
button_frame2.pack(pady=5)


restart_button = ttk.Button(button_frame2, text="Restart Bot", command=restart_bot)
restart_button.pack(side="left", padx=(0, 5))

terminal_button = ttk.Button(
    button_frame2, text="Show Terminal", command=toggle_terminal
)
terminal_button.pack(side="left", padx=(0, 5))

message_label = ttk.Label(root, textvariable=message_var, justify="center")
message_label.pack(pady=20)

load_info()

# look for dependencies folder
# either in the same directory or in the macOS directory
if (
    not os.path.exists("macOS/dependencies.py")
    or not os.path.exists("macOS/chronos.py")
    or not os.path.exists("macOS/updater.py")
):
    message_var.set(
        "Dependencies not found. \nPlease download dependencies from the GitHub repository."
    )
    run_button.config(state="disabled")
    stop_button.config(state="disabled")
    terminal_button.config(state="disabled")
    restart_button.config(state="disabled")
    save_button.config(state="disabled")
    room_option.config(state="disabled")
    building_option.config(state="disabled")
    roomName_label.config(state="disabled")
    username_entry.config(state="disabled")
    password_entry.config(state="disabled")
    date_entry.config(state="disabled")
    startTime_label.config(state="disabled")
    endTime_label.config(state="disabled")
    liveMode_checkbox.config(state="disabled")

# working on Live Mode
liveMode_checkbox.config(state="disabled")
root.mainloop()
