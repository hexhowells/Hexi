# import interfaces here
import starfield
import vlc
import time
import multiprocessing as mp
from hexi.interfaces.button import Button
from hexi.interfaces.speaker import sound


# entry point of skill
def start(command=None):
    audio_url = "http://lofi.stream.laut.fm/lofi?t302=2022-10-16_19-42-25&uuid=1be943bb-c5bf-486b-adb1-2c19e96c01dd"
   
    curr_volume = sound.get_volume()
    if curr_volume > 50:
        sound.set_volume(50)

    stream = vlc.MediaPlayer(audio_url)
    stream.play()
    
    starfield.start_animation()
    
    stream.stop()

    return 0


if __name__ == "__main__":
    start()
