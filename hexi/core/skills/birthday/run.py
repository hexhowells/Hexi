# import interfaces here
from hexi.interfaces.display import display, icons
import time


# entry point of skill
def start(command=None):
    screen = display.Display()
    screen.show_icon(icons.Cake)
    time.sleep(5)


if __name__ == "__main__":
    start()
