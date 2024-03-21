import os
import sys
import time
import requests
import platform
import subprocess
import tkinter as tk
from tkinter import ttk

APPVERSION = "v1.1"
scriptName = "bookingbot.py"
appName = "BookingBotApp.py"
# Check for updates ---------------------------------------------------------
isRunningFromSource = False
info_file = "data.rin"
terminal_shown = False
# Check if we are running from source
if (
    os.path.exists("INFOS.md")
    or os.path.exists("LICENSE.txt")
    or os.path.exists("README.md")
):
    isRunningFromSource = True
else:
    isRunningFromSource = False

# check if user has the bookingbot.py script, if not,
scriptVersion = ""
if isRunningFromSource == False:
    if not os.path.exists(scriptName):
        url = "https://raw.githubusercontent.com/rin-williams/UBCOBookingBot/main/bookingbot.py"
        response = requests.get(url)
        if response.status_code == 200:
            if not os.path.exists(scriptName):
                response = requests.get(url)
                with open(scriptName, "w") as file:
                    file.write(response.text)
    else:
        url = "https://raw.githubusercontent.com/rin-williams/UBCOBookingBot/main/bookingbot.py"
        response = requests.get(url)
        if response.status_code == 200:
            github_script = response.text
            with open(scriptName, "r") as file:
                local_script = file.read()
            if not local_script == github_script:
                print("Update is avaiable, fetching update from GitHub...")
                with open(scriptName, "w") as file:
                    file.write(github_script)
                    print("Your script has been updated, please restart the app")
                    time.sleep(5)
                    sys.exit()

# check for BookingBotApp.py updates
appVer = ""
if isRunningFromSource == False:
    url = "https://raw.githubusercontent.com/rin-williams/UBCOBookingBot/main/BookingBotApp.py"
    response = requests.get(url)
    if response.status_code == 200:
        github_app_script = response.text
        with open(appName, "r") as file:
            local_app_script = file.read()
            if "APPVERSION = " in local_app_script:
                appVer = local_app_script.split("=")[1].strip().strip('"')
        if not local_app_script == github_app_script:
            print("Update is avaiable, fetching update from GitHub...")
            with open(appName, "w") as file:
                file.write(github_app_script)
                print("Your app has been updated, please restart the app")
                time.sleep(5)
                sys.exit()
print("bookingbot.py is up to date")
print("BookingBotApp.py is up to date")
# ---------------------------------------------------------------------------


# App -----------------------------------------------------------------------


root = tk.Tk()
root.title("UBCO Booking Bot App v" + APPVERSION)
root.geometry("400x450")
root.resizable(False, False)

welcome_message = ttk.Label(root, text="Welcome!")
welcome_message.pack(pady=10)

username_frame = ttk.Frame(root)
username_frame.pack(pady=10)

username_label = ttk.Label(username_frame, text="Username:")
username_label.pack(side="left", padx=(0, 10))
username_entry = ttk.Entry(username_frame)
# set username to the last used username
if os.path.exists(info_file):
    with open(info_file, "r") as file:
        for line in file:
            if "username" in line:
                username_entry.insert(0, line.split("=")[1].strip())
                break
username_entry.pack(side="left")

password_frame = ttk.Frame(root)
password_frame.pack(pady=10)

password_label = ttk.Label(password_frame, text="Password:")
password_label.pack(side="left", padx=(0, 10))
password_entry = ttk.Entry(password_frame, show="*")
# set password to the last used password
if os.path.exists(info_file):
    with open(info_file, "r") as file:
        for line in file:
            if "password" in line:
                password_entry.insert(0, line.split("=")[1].strip())
                break
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
# set building to the last used building
if os.path.exists(info_file):
    with open(info_file, "r") as file:
        for line in file:
            if "com" in line:
                floor_number = line.split("=")[1].strip()[
                    0
                ]  # Get the first digit of the room number
                if floor_number == "0":
                    building_option.set("Commons: Floor 0")
                elif floor_number == "1":
                    building_option.set("Commons: Floor 1")
                elif floor_number == "3":
                    building_option.set("Commons: Floor 3")
                break
            elif "eme1" in line:
                building_option.set("EME: Tower 1")
                break
            elif "eme2" in line:
                building_option.set("EME: Tower 2")
                break
            elif "lib" in line:
                building_option.set("Library")
                break
building_option.pack(side="left")

room_frame = ttk.Frame(root)
room_frame.pack(pady=10)

room_label = ttk.Label(room_frame, text="Room:")
room_label.pack(side="left", padx=(0, 10))
room_option = ttk.Combobox(room_frame, state="readonly")
# set room to the last used room
if os.path.exists(info_file):
    with open(info_file, "r") as file:
        for line in file:
            if "lastUsedRoom" in line:
                room_option.set(line.split("=")[1].strip())
                break
room_option.pack(side="left")

roomName_frame = ttk.Frame(root)
roomName_frame.pack(pady=10)

roomName_label = ttk.Label(roomName_frame, text="Room name:")
roomName_label.pack(side="left", padx=(0, 10))
roomName_label = ttk.Entry(roomName_frame)
# set room name to the last used room name
if os.path.exists(info_file):
    with open(info_file, "r") as file:
        for line in file:
            if "roomName" in line:
                roomName_label.insert(0, line.split("=")[1].strip())
                break
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
    global f
    global running
    room_number = ""
    if not running:
        if (
            building_option.get() != ""
            and room_option.get() != ""
            and roomName_label.get() != ""
            and username_entry.get() != ""
            and password_entry.get() != ""
            and roomName_label.get() != ""
        ):
            running = True
            run_button.config(state="disabled")
            stop_button.config(state="normal")

            with open(info_file, "w") as file:
                building = building_option.get()
                file.write("lastUsedRoom=" + room_option.get() + "\n")
                room_number = room_option.get().split(" ")[1]
                if "Commons" in building:
                    file.write("com=" + room_number + "\n")
                elif "EME: Tower 1" in building:
                    file.write("eme1=" + room_number + "\n")
                elif "EME: Tower 2" in building:
                    file.write("eme2=" + room_number + "\n")
                elif "Library" in building:
                    file.write("lib=" + room_number + "\n")

                file.write("username=" + username_entry.get() + "\n")
                file.write("password=" + password_entry.get() + "\n")
                file.write("roomName=" + roomName_label.get() + "\n")
                file.truncate()

            # run the bot if on mac
            if platform.system() == "Darwin":
                print("\n\nALERT: Bot started.")
                message_var.set("Running bot...")
                subprocess.Popen(
                    [
                        "python3",
                        "bookingbot.py",
                    ]
                )
                message_var.set(
                    "Bot is running in terminal.\nPlease do not close the terminal window."
                    + "\nIf you want to stop the bot, click the 'Stop bot' button."
                )
            else:
                print("\n\nALERT: Oops! Your OS is not supported yet!")
                message_var.set("Oops! Your OS is not supported yet!")
        else:
            message_var.set("Please fill in all the fields.")


def stop_bot():
    global running
    if running:
        message_var.set("Bot stopped.")
        running = False
        run_button.config(state="normal")
        stop_button.config(state="disabled")
    # stop the bot if on mac
    if platform.system() == "Darwin":
        script = """
                do shell script "pkill -f bookingbot.py"
                tell application "Terminal"
                    set miniaturized of front window to false
                end tell
                """
        subprocess.run(["osascript", "-e", script])
        print("ALERT: Bot stopped.")


def show_terminal():
    if platform.system() == "Darwin":
        script = """
        tell application "Terminal"
            set miniaturized of front window to false
        end tell
        """
        subprocess.run(["osascript", "-e", script])


def hide_terminal():
    if platform.system() == "Darwin":
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


button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

button_frame2 = ttk.Frame(root)
button_frame2.pack(pady=5)

run_button = ttk.Button(button_frame, text="Start Bot", command=run_bot)
run_button.pack(side="left", padx=(0, 10))

stop_button = ttk.Button(
    button_frame, text="Stop Bot", command=stop_bot, state="disabled"
)
stop_button.pack(side="left", padx=(0, 10))

restart_button = ttk.Button(button_frame2, text="Restart Bot", command=restart_bot)
restart_button.pack(side="left", padx=(0, 10))

terminal_button = ttk.Button(
    button_frame2, text="Show Terminal", command=toggle_terminal
)
terminal_button.pack(side="left", padx=(0, 10))

message_label = ttk.Label(root, textvariable=message_var, justify="center")
message_label.pack(pady=10)

root.mainloop()
