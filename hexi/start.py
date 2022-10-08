import importlib
from PIL import Image
import subprocess
import os
import sys
import time
import random
from threading import Thread

from speech.speech import STT
from speech.wakeword import KeywordDetection

from interfaces.speaker import sound
from hexi.interfaces.display import display
from hexi import config

from core.intent.harpie import Harpie


class PauseToken:
    def __init__(self):
        self.pause_state = False

    def is_paused(self):
        return self.pause_state

    def pause(self):
        print("paused")
        self.pause_state = True

    def unpause(self):
        print("unpaused")
        self.pause_state = False

    def __str__(self):
        return str(self.pause_state)


def cycle_faces(token, screen):
    sleep_face = Image.open("assets/face/sleep-face.png")
    default_face = Image.open("assets/face/face.png")

    while True:
        if token.is_paused():
            continue
        else:
            #random_time = random.randint(10, 120)
            random_time = 5

            time.sleep(random_time)
            if not token.is_paused():
                screen.show_image(sleep_face)

            time.sleep(random_time)
            if not token.is_paused():
                screen.show_image(default_face)


class Hexi:
    def __init__(self):
        self.screen = display.Display()
        splash_screen = Image.open("assets/splashscreen.png")
        self.default_face = Image.open("assets/face/face.png")
        self.screen.show_image(splash_screen)

        self.stt = STT()
        self.harpie = Harpie("core/skills/skills.json")
        self.listener = KeywordDetection(callback=True)

        self.config = config.load()

        self.token = PauseToken()
        t1 = Thread(target=cycle_faces, args=(self.token, self.screen,))
        t1.start()

        subprocess.call(["boot/audio.sh"])
    

    def _show_face(self, y=0):
        self.screen.show_image(self.default_face, y=y)


    def idle(self):
        self._show_face()
        self.listener.run(self.listening_callback)
        print("after callback")
        

    def listening_callback(self):
        print("keyword detected!")

        self.token.pause()

        self._show_face(y=-5)
        sound.play_wav("assets/audio/beep.wav")
        command = self.stt.listen()
        print(command)
        
        self.process_command(command)


    def process_command(self, command):
        intent = self.harpie.get_intent(command)

        if len(intent) > 1:
            print("intent not found")
            self.token.unpause()
        else:
            self.start_skill(intent, command)
        
        self._show_face()


    def start_skill(self, intent, command):
        intent_name = intent[0].name
        cur_dir = os.getcwd()

        intent_dir = os.getcwd() + f"/core/skills/{intent_name}/"
        sys.path.append(intent_dir)
        os.chdir(intent_dir)

        print(intent_name)
        filepath = f'core.skills.{intent_name}.run'
        script = importlib.import_module(filepath, package=None)
        script.start(command)
        
        sys.path.append(cur_dir)
        os.chdir(cur_dir)
        self.token.unpause()
    


if __name__ == "__main__":
    hexi = Hexi()
    hexi.idle()

