import importlib
from PIL import Image
import subprocess

from speech.speech import STT
from speech.wakeword import KeywordDetection

from interfaces.speaker import sound
from hexi.interfaces.display import display

from core.intent.harpie import Harpie


class Hexi:
    def __init__(self):
        self.screen = display.Display()
        splash_screen = Image.open("assets/splashscreen.png")
        self.default_face = Image.open("assets/face/face.png")
        self.screen.show_image(splash_screen)

        self.stt = STT()
        self.harpie = Harpie("core/skills/skills.json")
        self.listener = KeywordDetection(callback=True)

        subprocess.call(["boot/audio.sh"])


    def idle(self):
        face_img = self.screen.show_image(self.default_face)
        self.listener.run(self.listening_callback)
        

    def listening_callback(self):
        print("keyword detected!")
        sound.play_wav("assets/audio/beep.wav")
        command = self.stt.listen()
        print(command)
        
        self.process_command(command)


    def process_command(self, command):
        intent = self.harpie.get_intent(command)

        if len(intent) > 1:
            print("intent not found")
        else:
            self.start_skill(intent, command)


    def start_skill(self, intent, command):
        print(intent[0].name)
        filepath = f'core.skills.{intent[0].name}.run'
        script = importlib.import_module(filepath, package=None)
        script.start(command)


if __name__ == "__main__":
    hexi = Hexi()
    hexi.idle()

