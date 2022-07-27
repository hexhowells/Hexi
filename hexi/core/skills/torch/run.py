# import interfaces here
from hexi.interfaces.display import display


# entry point of skill
def start(command=None):
    screen = display.Display()
    screen.set_contrast(255)
    screen.draw_rectangle(0, 0, 64, 128)
    while True:
        pass


if __name__ == "__main__":
    start()
