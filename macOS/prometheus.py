# prometheus is a GUI for atlanta.py, which is a bot that books study rooms in UBCO's library.

from datetime import datetime
import os
import re
import sys
import time
import requests
import platform
import subprocess
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

APPVERSION = "V0"
scriptName = "atalanta.py"
appName = "prometheus.py"
info_file = "data.rin"

root = tk.Tk()
root.title("prometheus " + APPVERSION)
root.geometry("600x550")
root.resizable(False, False)


welcome_message = "welcome to prometheus " + APPVERSION
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
    if building.get() == "EME: Tower 1":
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
                    "macOS/dependencies/chronos.py",
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
        script = """
                do shell script "pkill -f atalanta.py"
                tell application "Terminal"
                    set miniaturized of front window to false
                end tell
                """
        subprocess.run(["osascript", "-e", script])
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
    if platform.system() == "Darwin":
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
    with open(info_file, "w") as file:
        file.write("username=" + username_entry.get() + "\n")
        file.write("password=" + password_entry.get() + "\n")
        file.write("roomName=" + roomName_label.get() + "\n")
        file.write("building=" + building_option.get() + "\n")
        file.write("room=" + room_option.get() + "\n")
        file.write("date=" + date_entry.get() + "\n")
        file.write("startTime=" + startTime.get() + "\n")
        file.write("endTime=" + endTime.get() + "\n")
        file.truncate()
        message_var.set("Info saved in " + info_file + " file")


def load_info():
    global username
    global welcome_message

    with open(info_file, "r") as file:
        for line in file:
            if "username" in line:
                username = line.split("=")[1].strip()
                username_entry.insert(0, username)
            elif "password" in line:
                password = line.split("=")[1].strip()
                password_entry.insert(0, password)
            elif "roomName" in line:
                roomName = line.split("=")[1].strip()
                roomName_label.insert(0, roomName)
            elif "building" in line:
                building.set(line.split("=")[1].strip())
            elif "room" in line:
                room_option.set(line.split("=")[1].strip())
            elif "startTime" in line:
                startTime.set(line.split("=")[1].strip())
            elif "endTime" in line:
                endTime.set(line.split("=")[1].strip())
            elif "date" in line:
                date = line.split("=")[1].strip()
                date_entry.insert(0, date)


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
    start_time = startTime.get()
    start_index = availableTimes.index(start_time)
    end_times = availableTimes[start_index + 1 : start_index + 13]
    endTime.set("")  # clear current selection
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

liveMode_button = ttk.Button(
    button_frame2, text="Live Mode", command=run_bot, state="disabled"
)
liveMode_button.pack(side="left", padx=(0, 5))


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
if not os.path.exists("macOS/dependencies"):
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

root.mainloop()
