# updater is a prometheus and chronos, and dependencies
# it pulls update from
# https://raw.githubusercontent.com/rin-williams/prometheus/main/macOS/

import requests
import os


def update_prometheus():
    url = "https://raw.githubusercontent.com/rin-williams/prometheus/main/macOS/prometheus.py"
    response = requests.get(url)
    with open("macOS/prometheus.py", "w") as file:
        file.write(response.text)
    print("Prometheus has been updated.")


def update_chronos():
    url = "https://raw.githubusercontent.com/rin-williams/chronos/main/macOS/dependencies/chronos.py"
    response = requests.get(url)
    with open("macOS/dependencies/chronos.py", "w") as file:
        file.write(response.text)
    print("Chronos has been updated.")


def update_dependencies():
    url = "https://raw.githubusercontent.com/rin-williams/chronos/main/macOS/dependencies/dependencies.py"
    response = requests.get(url)
    with open("macOS/dependencies/dependencies.py", "w") as file:
        file.write(response.text)
    print("Dependencies has been updated.")


update_prometheus()
update_chronos()
update_dependencies()
