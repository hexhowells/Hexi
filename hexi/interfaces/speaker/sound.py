import simpleaudio as sa
import alsaaudio


def play_wav(wav_filepath):
    wave_obj = sa.WaveObject.from_wave_file(wav_filepath)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    return True


def set_volume(volume):
    volume = min(volume, 100)
    volume = max(volume, 20)

    mixer = alsaaudio.Mixer()
    mixer.setvolume(volume)


def get_volume():
    mixer = alsaaudio.Mixer()
    return mixer.getvolume()[0]
