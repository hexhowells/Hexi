# import interfaces here
from hexi.interfaces.motor import Motor


# entry point of skill
def start(command=None):
    motor = Motor()
    motor.drive(Motor.FORWARD, 0.5)
    motor.drive(Motor.BACKWARD, 0.4)


if __name__ == "__main__":
    start()
