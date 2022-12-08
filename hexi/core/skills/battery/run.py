# import interfaces here
import time
import sys
from hexi.interfaces.battery import Battery
from hexi.interfaces.display import display, icons


# entry point of skill
def start(command=None):
    screen = display.Display()
    battery = Battery()
    print(battery.voltage())
    level = battery.percentage()
    battery_info = str(level) + "%"

    screen.draw_text_custom(battery_info, 25, 15, 36)
    time.sleep(5)



if __name__ == "__main__":
    command = sys.argv[1:]
    if len(command) == 0: command = None
    start(command)
