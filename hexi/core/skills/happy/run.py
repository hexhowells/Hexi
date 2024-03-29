# import interfaces here
import time
from hexi.interfaces.motor import Motor
from hexi.interfaces.display import display
from PIL import Image


# entry point of skill
def start(command=None):
    motor = Motor()
    screen = display.Display()

    face_image = Image.open("../../../assets/face/happy-face.png")
    screen.show_image(face_image)

    motor.drive(Motor.LEFT, 0.05)
    time.sleep(0.1)

    for _ in range(3):
        motor.drive(Motor.RIGHT, 0.1)
        time.sleep(0.1)
        motor.drive(Motor.LEFT, 0.1)
        time.sleep(0.1)

    motor.drive(Motor.RIGHT, 0.05)
    time.sleep(1)


if __name__ == "__main__":
    start()
