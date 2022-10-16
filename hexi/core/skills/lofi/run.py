# import interfaces here
from hexi.interfaces.speaker import sound
#import rain
import starfield
import vlc


# entry point of skill
def start(command=None):
    audio_url = "http://lofi.stream.laut.fm/lofi?t302=2022-10-16_19-42-25&uuid=1be943bb-c5bf-486b-adb1-2c19e96c01dd"
    
    stream = vlc.MediaPlayer(audio_url)
    stream.play()
    
    #rain.start_animation()
    starfield.start_animation()


if __name__ == "__main__":
    start()
