from hexi.interfaces.motor import Motor


def start(command):
    motor = Motor()
    motor.drive(Motor.FORWARD, 0.5)


if __name__ == "__main__":
    start()
