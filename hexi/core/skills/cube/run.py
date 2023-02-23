import time
from PIL import Image

from hexi.features.fiducial import find_marker
from hexi.interfaces.camera import camera
from hexi.interfaces.motor import Motor
from hexi.interfaces.button import Button
from hexi.interfaces.display import display


def start(command=None):
    screen = display.Display()

    assets_path = "/home/pi/Hexi/hexi/assets/face/"
    default_face = Image.open(assets_path + "face.png")
    happy_face = Image.open(assets_path + "happy-face.png")
    sad_face = Image.open(assets_path + "sad-face.png")
    screen.show_image(default_face)

    cam = camera.Camera()
    motor = Motor()
    center_x = 320
    tolerance = 50
    btn = Button()
    sad_timer = 250

    for i, frame in enumerate(cam.stream()):
        if btn.pushed():
            break

        # cube cant be found
        if ((i+1) % sad_timer) == 0:
            screen.show_image(sad_face)
            time.sleep(3)
            break

        if (i % 5) != 0:
            continue

        image = frame.array
        marker_points, marker_sizes = find_marker(image)
        
        # cube seen
        if len(marker_points) > 0:
            cX, _ = marker_points[0]
            m_size = marker_sizes[0]
            sad_timer += 200  # delay the robot giving up

            tolerance = 50 if m_size < 65 else 80

            # cube found
            if m_size > 280:
                screen.show_image(happy_face)
                for _ in range(6):
                    motor.drive(Motor.RIGHT, 0.1)
                    time.sleep(0.05)
                    motor.drive(Motor.LEFT, 0.1)
                    time.sleep(0.05)
                break

            # cube seen, move towards or adjust alignment
            if cX < (center_x - tolerance):
                motor.drive(Motor.LEFT, 0.05)
            elif cX > (center_x + tolerance):            
                motor.drive(Motor.RIGHT, 0.05)
            else:
                motor.drive(Motor.FORWARD, 0.3)
        else:
            # search for cube
            motor.drive(Motor.RIGHT, 0.05)



if __name__ == "__main__":
    start()
