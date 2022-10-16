import importlib
from PIL import Image
import subprocess
import os
import sys
import time
import random
from threading import Thread
import multiprocessing as mp
import psutil
import atexit

from speech.speech import STT
from speech.wakeword import KeywordDetection

from interfaces.speaker import sound
from hexi.interfaces.display import display
from hexi import config

from core.intent.harpie import Harpie


class PauseToken:
    def __init__(self):
        self.pause_state = False
        self.kill = False

    def is_paused(self):
        return self.pause_state

    def pause(self):
        print("paused")
        self.pause_state = True

    def unpause(self):
        print("unpaused")
        self.pause_state = False

    def kill(self):
        self.kill = True

    def __str__(self):
        return str(self.pause_state)


def cycle_faces(token, screen):
    sleep_face = Image.open("assets/face/sleep-face.png")
    default_face = Image.open("assets/face/face.png")

    while not token.kill:
        if token.is_paused():
            continue
        else:
            random_time = random.randint(10, 120)

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
        face_cycle_thread = Thread(target=cycle_faces, args=(self.token, self.screen,))
        face_cycle_thread.start()

        self.process_handler = None
        self.skill_mp = None

        subprocess.call(["boot/audio.sh"])

        atexit.register(self._exit)


    def _exit(self):
        if self.skill_mp and self.skill_mp.is_alive():
            self.skill_mp.terminate()
            self.skill_mp.join()

        self.token.kill()
    

    def _show_face(self, y=0):
        self.screen.show_image(self.default_face, y=y)


    def idle(self):
        self._show_face()
        self.listener.run(self.listening_callback)
        print("after callback")
        

    def listening_callback(self):
        print("keyword detected!")

        if self.process_handler:
            self.process_handler.suspend() # pause skill process

        self.token.pause()  # pause face cycle thread

        self._show_face(y=-5)
        sound.play_wav("assets/audio/beep.wav")
        command = self.stt.listen()
        print(command)
        
        self.process_command(command)


    def process_command(self, command):
        if command == "stop":
            print("[stop command] - stopping background skill")
            if self.skill_mp and self.skill_mp.is_alive():
                self.skill_mp.terminate()
            self.skill_mp = None
            self.process_handler = None
            self._show_face()
            return 0


        intent = self.harpie.get_intent(command)

        if len(intent) > 1:
            print("intent not found")
            self.token.unpause()

            if self.process_handler:
                self.process_handler.resume()

            self._show_face()
        else:
            if self.skill_mp and self.skill_mp.is_alive():
                print("terminating background skill")
                self.skill_mp.terminate()
                print("background skill terminated!")

            self.skill_mp = mp.Process(target=self.start_skill, args=(intent, command))
            self.skill_mp.start()
            self.process_handler = psutil.Process(self.skill_mp.pid)
#            self.start_skill(intent, command)



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

        self._show_face()
    


if __name__ == "__main__":
    hexi = Hexi()
    hexi.idle()

