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

from hexi.interfaces.speaker import sound
from hexi.interfaces.display import display, icons
from hexi.interfaces.battery import Battery
from hexi import config
from telegram import listener

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
    happy_face = Image.open("assets/face/happy-face.png")

    while True:
        if token.is_paused():
            continue
        else:
            random_time = random.randint(10, 120)
            gamma = random.uniform(0, 1)

            time.sleep(random_time)
            if not token.is_paused():
                if gamma < 0.8:
                    screen.show_image(sleep_face, y=10)
                elif gamma < 0.90:
                    screen.show_image(happy_face)
                    random_time = 8
                else:
                    screen.show_icon(icons.Heart)
                    random_time = 8

            time.sleep(random_time)
            if not token.is_paused():
                screen.show_image(default_face)


def monitor_battery(token, screen, voltage_lim=3.335):
    battery = Battery()
    while True:
        time.sleep(10)
        voltage = battery.voltage()

        if voltage < voltage_lim:
            token.pause()
            screen.show_icon(icons.BatteryLow)


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

        telebot_thread = Thread(target=listener.start_bot, args=(self.token, ))
        telebot_thread.start()

        battery_thread = Thread(target=monitor_battery, args=(self.token, self.screen))
        battery_thread.start()

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
        command = command.replace("'", "")  # normalise command
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

