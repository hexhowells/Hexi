import RPi.GPIO as gpio
import time


class Motor:
    FORWARD = [False, True, True, False]
    BACKWARD = [True, False, False, True]
    RIGHT = [True, False, True, False]
    LEFT = [False, True, False, True]

    def __init__(self, pins=[13, 15, 16, 18]):
        self.pins = pins

        gpio.setmode(gpio.BOARD)
        gpio.setup(self.pins[0], gpio.OUT)
        gpio.setup(self.pins[1], gpio.OUT)
        gpio.setup(self.pins[2], gpio.OUT)
        gpio.setup(self.pins[3], gpio.OUT)


    def drive(self, direction, seconds=None):
        for pin, direc in zip(self.pins, direction):
            gpio.output(pin, direc)

        if seconds:
            time.sleep(seconds)

            for pin in self.pins:
                gpio.output(pin, False)


    def stop(self):
        for pin in self.pins:
            gpio.output(pin, False)


    def __del__(self):
        self.stop()
        gpio.cleanup()


