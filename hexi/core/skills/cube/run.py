import time

from hexi.features.fiducial import find_marker
from hexi.interfaces.camera import camera
from hexi.interfaces.motor import Motor


def start(command=None):
    cam = camera.Camera()
    motor = Motor()
    center_x = 320
    tolerance = 50

    for i, frame in enumerate(cam.stream()):
        if (i % 5) != 0:
            continue

        #print("\ntaking picture")
        image = frame.array
        marker_points, marker_sizes = find_marker(image)

        if len(marker_points) > 0:
            cX, _ = marker_points[0]
            m_size = marker_sizes[0]

            tolerance = 50 if m_size < 65 else 80

            if m_size > 280:
                for _ in range(6):
                    motor.drive(Motor.RIGHT, 0.1)
                    time.sleep(0.05)
                    motor.drive(Motor.LEFT, 0.1)
                    time.sleep(0.05)
                break

            if cX < (center_x - tolerance):
                motor.drive(Motor.LEFT, 0.05)
            elif cX > (center_x + tolerance):            
                motor.drive(Motor.RIGHT, 0.05)
            else:
                motor.drive(Motor.FORWARD, 0.3)
            #print(f'{cX=}  {m_size=}  {tolerance=}')
        else:
            # search for cube
            motor.drive(Motor.RIGHT, 0.05)



if __name__ == "__main__":
    start()
