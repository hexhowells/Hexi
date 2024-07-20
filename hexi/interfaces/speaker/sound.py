import simpleaudio as sa
import alsaaudio
from playsound import playsound


class Sound:
    def __init__(self, wav_filepath):
        self.wave_obj = sa.WaveObject.from_wave_file(wav_filepath)

    def play(self):
        self.play_obj = self.wave_obj.play()
        self.play_obj.wait_done()

    def stop(self):
        stop_obj = self.play_obj.stop()



def play_wav(wav_filepath):
    wave_obj = sa.WaveObject.from_wave_file(wav_filepath)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def play_extended_sound(filepath):
    playsound(filepath)
    return True


def set_volume(volume):
    volume = min(volume, 100)
    volume = max(volume, 20)

    mixer = alsaaudio.Mixer()
    mixer.setvolume(volume)


def get_volume():
    mixer = alsaaudio.Mixer()
    return mixer.getvolume()[0]
