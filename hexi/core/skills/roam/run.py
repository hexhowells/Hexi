from hexi.interfaces.camera import camera
from hexi.interfaces.motor import Motor
from hexi.interfaces.display import display
from hexi.interfaces.button import Button

from curiosity import NewObject
from drive import Drive
from cube import FindCube

import time
from PIL import Image
import random


# dance when cube is found
def dance(motor):
    for _ in range(6):
        motor.drive(Motor.RIGHT, 0.1)
        time.sleep(0.05)
        motor.drive(Motor.LEFT, 0.1)
        time.sleep(0.05)


def start(command=None):
    cam = camera.Camera()
    motor = Motor()
    screen = display.Display()

    assets_path = "/home/pi/Hexi/hexi/assets/face/"
    default_face = Image.open(assets_path + "face.png")
    curious_face = Image.open(assets_path + "curious-face.png")
    happy_face = Image.open(assets_path + "happy-face.png")
    angry_face = Image.open(assets_path + "angry-face.png")

    screen.show_image(default_face)

    cube = FindCube()
    drive = Drive()
    obj = NewObject()

    drive_gamma = 0.4
    cube_gamma = 0.9
    angry_gamma = 0.2
    obj_gamma = 0.9

    prev_moved = False

    # move motors to indicate roaming mode has started
    motor.drive(Motor.FORWARD, 0.1)
    motor.drive(Motor.BACKWARD, 0.1)

    btn = Button()
    

    for i, frame in enumerate(cam.stream()):
        if btn.pushed():
            break

        if (i % 30) != 0:
            continue

        image = frame.array

        drive_action, drive_action_len = drive.compute_path(image)
        new_object = obj.detect(image)
        cube_found, cube_action, cube_action_len = cube.find(image)
        
        if cube_found and (random.uniform(0, 1) < cube_gamma):
            print("\t CUBE FOUND")
            if cube_action:
                motor.drive(cube_action, cube_action_len)
            else:
                screen.show_image(happy_face)
                dance(motor)
                screen.show_image(default_face)
                prev_moved = True
            continue


        if new_object and not prev_moved and (random.uniform(0, 1) < obj_gamma):
            print("\tNEW OBJECT")
            motor.drive(Motor.BACKWARD, 0.1)

            if random.uniform(0, 1) < angry_gamma:
                screen.show_image(angry_face)
                motor.drive(Motor.FORWARD, 0.2)
            else:
                screen.show_image(curious_face)

            time.sleep(4)
            screen.show_image(default_face)
            continue


        if random.uniform(0, 1) < drive_gamma:
            print("\t DRIVE")
            motor.drive(drive_action, drive_action_len)
            prev_moved = True
            continue

        prev_moved = False
        print("\t NOTHING")

    cam.close()

    motor.drive(motor.BACKWARD, 0.1)
    motor.drive(motor.FORWARD, 0.1)

    return 0



if __name__ == "__main__":
    start()
        

    
