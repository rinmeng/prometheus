# chronos.py is the backbones of prometheus.py where everything runs.
# this is the brain of the operation

import os
import subprocess

info_file = "data.rin"
# check if user has all the required libraries
with open(info_file, "r") as file:
    data = file.read()
    if "hasRequiredLibraries=True" in data:
        print("All required libraries are installed.")
    else:
        subprocess.run(["python3", "macOS/dependencies/dependencies.py"])
        with open(info_file, "a") as file:
            file.write("hasRequiredLibraries=True")
            file.close()
