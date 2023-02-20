# import interfaces here
from hexi.interfaces.speaker import sound
from hexi.interfaces.motor import Motor
from hexi.interfaces.button import Button

from threading import Thread
import multiprocessing
import time
import random


def dance(motor):
    seq_1 = [(Motor.RIGHT,0.5), (Motor.LEFT,0.5)]
    seq_2 = [(Motor.FORWARD,0.5), (Motor.BACKWARD,0.5)]
    btn = Button()

    time.sleep(3)

    for i in range(6):
        if btn.pushed(): break

        steps = random.randint(1, 3)
        for i in range(steps):
            for direc, secs in seq_1:
                if btn.pushed(): break
                motor.drive(direc, secs)
                time.sleep(0.38)

        for direc, secs in seq_2:
            if btn.pushed(): break
            motor.drive(direc, secs)
            time.sleep(0.4)


# entry point of skill
def start(command=None):
    motor = Motor()
    audio = sound.Sound("dance_music.wav")
    
    music_thread = Thread(target=audio.play)
#    music_thread = Thread(target=sound.play_wav, args=("dance_music.wav", ))
    music_thread.start()
    
    dance(motor)
    
    audio.stop()
    

if __name__ == "__main__":
    start()
