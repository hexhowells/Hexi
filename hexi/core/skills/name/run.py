# import interfaces here
import time
import threading
from PIL import Image
from hexi.interfaces.speaker import sound
from hexi.interfaces.display import display


# entry point of skill
def start(command=None):
    screen = display.Display()

    t = threading.Thread(target=sound.play_wav, args=["name.wav"])
    t.start()

    face = Image.open("/home/pi/Hexi/hexi/assets/face/happy-face.png")
    screen.show_image(face)
    time.sleep(2)




if __name__ == "__main__":
    start()
