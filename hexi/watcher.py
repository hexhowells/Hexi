import subprocess
import time


def start():
    proc = subprocess.Popen(["python3", "start.py"])
    out, err = proc.communicate()

    print(f'[ERROR] - {err}')
    print("core has terminated, restarting...")
    time.sleep(2)


while True:
    start()
