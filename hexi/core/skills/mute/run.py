# import interfaces here
from hexi.interfaces.speaker import sound
from hexi.interfaces.display import display, icons
import time


# entry point of skill
def start(command=None):
    screen = display.Display()
    screen.show_icon(icons.VolumeOff)
    sound.set_volume(0)

    time.sleep(3)


if __name__ == "__main__":
    start()
