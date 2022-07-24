# import interfaces here
from hexi.interfaces.motor import Motor

# entry point of skill
def start(command):
    motor = Motor()
    motor.drive(Motor.RIGHT, 1.3)


if __name__ == "__main__":
    start()
