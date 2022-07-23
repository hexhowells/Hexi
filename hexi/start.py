import importlib
from PIL import Image
import subprocess

from speech.speech import STT
from speech.wakeword import KeywordDetection

from interfaces.speaker import sound
from interfaces.display import display
from core.intent.harpie import Harpie

print("loading STT model..")
stt = STT()

harpie = Harpie("core/skills/skills.json")

face_img_path = "assets/face/face.png"
face_img = Image.open(face_img_path)

subprocess.call(["boot/audio.sh"])


def run_script(intent):
    pass
    # os run or dynamically import to run script


def wakeword_callback():
    # audible indicator that wakeword has been recognised
    print("hello!")
    sound.play_wav("assets/audio/beep.wav")

    command = stt.listen()
    print(command)

    intent = harpie.get_intent(command)

    if len(intent) > 1:
        print("intent not found")
    else:
        print(intent[0].name)
        filepath = f'core.skills.{intent[0].name}.run'
        script = importlib.import_module(filepath, package=None)
        script.start()

    return True


def main():
    screen = display.Display()
    screen.show_image(face_img)
    print("loading wakeword listener..")
    listener = KeywordDetection(callback=True)
    listener.run(wakeword_callback)


if __name__ == "__main__":
    main()


