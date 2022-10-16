# import interfaces here
from hexi.interfaces.speaker import sound
import rain
import starfield
import vlc


# entry point of skill
def start(command=None):
    audio_url = "https://rainymood.com/audio1112/0.m4a"
    
    stream = vlc.MediaPlayer(audio_url)
    stream.play()
    
    rain.start_animation()
    #starfield.start_animation()


if __name__ == "__main__":
    start()
