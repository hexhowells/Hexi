# import interfaces here
import sys
import time
from hexi.interfaces.speaker import sound
from hexi.interfaces.display import display, icons


# entry point of skill
def start(command=None):
    screen = display.Display()
    if not command:
        return 0

    if "high" in command:
        sound.set_volume(100)
        screen.show_icon(icons.VolumeHigh)
    elif "low" in command:
        sound.set_volume(40)
        screen.show_icon(icons.VolumeLow)

    time.sleep(3)



if __name__ == "__main__":
    command = sys.argv[1:]
    if len(command) == 0: command = None
    start(command)
