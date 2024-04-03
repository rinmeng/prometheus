# all library used by prometheus_macOS.py
# library including
"""
from datetime import datetime
import os
import sys
import time
import requests
import platform
import subprocess
import tkinter as tk
from tkinter import ttk
"""

import os
import subprocess

# check if user has pip3 installed
if subprocess.run(["which", "pip3"], capture_output=True).returncode == 1:
    print("pip3 not installed. Please install pip3")
    subprocess.run(["sudo", "easy_install", "pip"])
else:
    print("pip3 detected")
if subprocess.run(["pip3", "show", "selenium"], capture_output=True).returncode == 1:
    print("Selenium library not installed. installing now...")
    subprocess.run(["pip3", "install", "selenium"])
else:
    print("Selenium library detected")
if subprocess.run(["pip3", "show", "requests"], capture_output=True).returncode == 1:
    print("Requests library not installed. installing now...")
    subprocess.run(["pip3", "install", "requests"])
else:
    print("Requests library detected")
