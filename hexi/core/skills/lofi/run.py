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
   
    #sound.set_volume(80)

    stream = vlc.MediaPlayer(audio_url)
    stream.play()
    
    #rain.start_animation()
    proc = mp.Process(target=starfield.start_animation)
    proc.start()

    btn = Button()
    while not btn.pushed():
        time.sleep(0.1)
    
    stream.stop()
    proc.kill()

    return 0


if __name__ == "__main__":
    start()
