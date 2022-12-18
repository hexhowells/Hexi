import RPi.GPIO as gpio
import time


class Button:
    def __init__(self, pin=24):
        self.pin = pin
        self.bouncetime = 0.2
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.pin, gpio.IN, pull_up_down=gpio.PUD_UP)


    def detect_push(self, callback):
        while True:
            if gpio.input(self.pin) == gpio.LOW:
                callback()
                time.sleep(self.bouncetime)


    def detect_hold(self, callback, args, seconds=3):
        prev_push_time = int(time.time())
        hold_ticks = 0
        while True:
            time.sleep(self.bouncetime)

            if gpio.input(self.pin) == gpio.LOW:
                push_time = int(time.time())
                
                if (push_time - prev_push_time) <= 1:
                    hold_ticks += 1
                else:
                    hold_ticks = 0

                if hold_ticks > (4 * seconds):
                    callback(*args)
                    hold_ticks = 0
                 
                prev_push_time = push_time

    def pushed(self):
        return gpio.input(self.pin) == gpio.LOW



