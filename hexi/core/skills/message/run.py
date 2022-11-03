# import interfaces here
import time
import sys
from hexi.interfaces.display import display


# entry point of skill
def start(command=None):
    with open("../../../telegram/messages.txt", "r+") as msg_file:
        message = msg_file.read()
        msg_file.seek(0)
        msg_file.truncate()
        msg_file.write("")

    screen = display.Display()

    if message == "":
        screen.draw_text_custom("No Messages!", x=6, y=25, size=18)
        time.sleep(3)
    else:
        terminal = display.Terminal(screen)
        terminal.type(message)
        time.sleep(5)
        terminal.clear()


if __name__ == "__main__":
    command = sys.argv[1:]
    if len(command) == 0: command = None
    start(command)
