# import interfaces here
from hexi.interfaces.speaker import sound
import threading
import rain
import starfield


# entry point of skill
def start(command=None):
    t1 = threading.Thread(target=sound.play_extended_sound, args=["assets/rain_sounds.wav"])
    t1.start()
    
    rain.start_animation()
    #starfield.start_animation()


if __name__ == "__main__":
    start()
