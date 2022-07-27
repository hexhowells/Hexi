import subprocess
import time


def start():
    proc = subprocess.Popen(["python3", "start.py"])
    out, err = proc.communicate()

    print("core has terminated, restarting...")
    time.sleep(2)


while True:
    start()
