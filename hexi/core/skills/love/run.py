# import interfaces here
from hexi.interfaces.display import display
from hexi.interfaces.display import icons
import time


# entry point of skill
def start(command=None):
    screen = display.Display()
    screen.show_icon(icons.Heart)
    time.sleep(3)


if __name__ == "__main__":
    start()
