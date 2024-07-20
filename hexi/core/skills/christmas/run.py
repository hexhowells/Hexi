# import interfaces here
import time
import sys
from PIL import Image
import threading

from hexi.interfaces.speaker import sound
from hexi.interfaces.display import display
from hexi.interfaces.motor import Motor
from hexi.interfaces.button import Button


# entry point of skill
def start(command=None):
    screen = display.Display(font="fontawesome2.ttf")
    motor = Motor()
    btn = Button()

    xmas_icons = ["\uf06b", "\uf2dc", "\uf786", "\uf7aa", "\uf7d0"]

    face_img = Image.open("../../../assets/face/happy-face.png")
    screen.show_image(face_img)
    
    audio = sound.Sound("xmas.wav")
    t1 = threading.Thread(target=audio.play)
    #t1 = threading.Thread(target=sound.play_wav, args=("xmas.wav",))
    t1.start()

    time.sleep(3)
    for i in range(5):
        motor.drive(Motor.RIGHT, 0.1)
        motor.drive(Motor.LEFT, 0.1)
        motor.drive(Motor.RIGHT, 0.1)
        motor.drive(Motor.LEFT, 0.1)

        time.sleep(2)
        if btn.pushed(): break
        screen.show_icon(xmas_icons[i])
        if btn.pushed(): break
        time.sleep(6)
        screen.show_image(face_img)
        if btn.pushed(): break
        time.sleep(2)
    
    audio.stop()


if __name__ == "__main__":
    command = sys.argv[1:]
    if len(command) == 0: command = None
    start(command)
