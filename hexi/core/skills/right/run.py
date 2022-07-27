# import interfaces here
from hexi.interfaces.motor import Motor


# entry point of skill
def start(command=None):
    motor = Motor()
    motor.drive(Motor.RIGHT, 0.5)


if __name__ == "__main__":
    start()
