import time
from hexi.interfaces.display import display, icons
from hexi.interfaces.speaker import sound


# entry point of skill
def start(command=None):
    screen = display.Display()
    screen.show_icon(icons.Cake)
    
    sound.play_wav("happy-birthday.wav")


if __name__ == "__main__":
    start()
