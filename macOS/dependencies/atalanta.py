# atlanta.py is the backbones of prometheus.py where everything runs.
# this is the brain of the operation

import os
import subprocess

# check if user has all the required libraries
subprocess.run(["python3", "macOS/dependencies/dependencies.py"])
