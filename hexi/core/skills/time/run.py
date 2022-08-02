# import interfaces here
from hexi.interfaces.display import display
import time


# entry point of skill
def start(command=None):
    current_time = time.localtime()
    processed_time = time.strftime("%I:%M", current_time)
    midday = time.strftime("%p", current_time)

    screen = display.Display()
    screen.draw_text_custom(processed_time, 8, 18, size=38)
    screen.draw_text_custom(midday, 106, 40, size=11)
    time.sleep(6)


if __name__ == "__main__":
    start()
