# import interfaces here
import time
import sys
from PIL import Image
import threading

from hexi.interfaces.speaker import sound
from hexi.interfaces.display import display
from hexi.interfaces.motor import Motor


# entry point of skill
def start(command=None):
    screen = display.Display(font="fontawesome2.ttf")
    motor = Motor()

    xmas_icons = ["\uf06b", "\uf2dc", "\uf786", "\uf7aa", "\uf7d0"]

    face_img = Image.open("../../../assets/face/happy-face.png")
    screen.show_image(face_img)

    t1 = threading.Thread(target=sound.play_wav, args=("xmas.wav",))
    t1.start()

    time.sleep(3)
    for i in range(5):
        motor.drive(Motor.RIGHT, 0.1)
        motor.drive(Motor.LEFT, 0.1)
        motor.drive(Motor.RIGHT, 0.1)
        motor.drive(Motor.LEFT, 0.1)

        time.sleep(2)
        screen.show_icon(xmas_icons[i])
        time.sleep(6)
        screen.show_image(face_img)
        time.sleep(2)


if __name__ == "__main__":
    command = sys.argv[1:]
    if len(command) == 0: command = None
    start(command)
