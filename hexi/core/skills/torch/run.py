# import interfaces here
from hexi.interfaces.display import display
from hexi.interfaces.button import Button


# entry point of skill
def start(command=None):
    screen = display.Display()
    screen.set_contrast(255)
    screen.draw_rectangle(0, 0, 64, 128)

    btn = Button()
    while not btn.pushed():
        pass


if __name__ == "__main__":
    start()
