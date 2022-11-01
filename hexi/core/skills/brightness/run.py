# import interfaces here
import time
import sys
from hexi.interfaces.display import display, icons


# entry point of skill
def start(command=None):
    if not command:
        return 0

    screen = display.Display()
    screen.show_icon(icons.Sun)
    time.sleep(1)

    if "high" in command:
        screen.set_contrast(255)
    elif "low" in command:
        screen.set_contrast(10)

    time.sleep(3)


if __name__ == "__main__":
    command = sys.argv[1:]
    if len(command) == 0: command = None
    start(command)
