# import interfaces here
from hexi.interfaces.speaker import sound
import rain
import starfield
import vlc
import time
import multiprocessing as mp
from hexi.interfaces.button import Button


# entry point of skill
def start(command=None):
    audio_url = "https://rainymood.com/audio1112/0.m4a"
    
    stream = vlc.MediaPlayer(audio_url)
    stream.play()
    
    proc = mp.Process(target=rain.start_animation)
    proc.start()

    btn = Button()
    while not btn.pushed():
        time.sleep(0.1)

    stream.stop()
    proc.kill()

    

if __name__ == "__main__":
    start()
