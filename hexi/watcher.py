import subprocess
import time
from hexi.interfaces.button import Button
from threading import Thread
from hexi.interfaces.display import display


def stop_core(proc):
    screen = display.Display()
    screen.draw_text("Restarting...")
    print("killing core from watcher")
    proc.kill()


def start():
    button = Button()

    proc = subprocess.Popen(["python3", "start.py"])
    t1 = Thread(target=button.detect_hold, args=(stop_core, (proc, )))
    t1.start()
    out, err = proc.communicate()

    print(f'[ERROR] - {err}')
    print("core has terminated, restarting...")
    time.sleep(2)


while True:
    start()
