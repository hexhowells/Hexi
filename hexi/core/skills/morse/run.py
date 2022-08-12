# import interfaces here
import time
import threading
from hexi.interfaces.display import display
from hexi.interfaces.speaker import sound


# entry point of skill
def start(command=None):
    screen = display.Display()

    t = threading.Thread(target=sound.play_wav, args=["morse.wav"])
    t.start()

    screen.draw_text_custom("--.-..-.", 17, 12, size=40)
    time.sleep(10)


if __name__ == "__main__":
    start()
