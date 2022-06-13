import os
from datetime import datetime
from threading import Thread

import pvporcupine
from pvrecorder import PvRecorder

import utils


class KeywordDetection(Thread):
    def __init__(
            self, 
            access_key=None, 
            library_path=pvporcupine.LIBRARY_PATH,
            model_path=pvporcupine.MODEL_PATH,
            keyword_path="hexi-keyword.ppn",
            sensitivities=[0.5],
            input_device_index=-1,
            callback = None
            ):
        super(KeywordDetection, self).__init__()

        if access_key:
            self._access_key = access_key
        else:
            self._access_key = utils.load_api_key()

        self._library_path = library_path
        self._model_path = model_path
        self._keyword_paths = [keyword_path]
        self._sensitivities = sensitivities
        self._input_device_index = input_device_index
        self._callback = callback

    
    def run(self):
        porcupine = None
        recorder = None

        try:
            porcupine = pvporcupine.create(
                access_key=self._access_key,
                library_path=self._library_path,
                model_path=self._model_path,
                keyword_paths=self._keyword_paths,
                sensitivities=self._sensitivities)

            recorder = PvRecorder(device_index=self._input_device_index, 
                                frame_length=porcupine.frame_length)
            recorder.start()

            print(f'Using device: {recorder.selected_device}')
            print('Listening...')

            while True:
                pcm = recorder.read()

                result = porcupine.process(pcm)

                if result >= 0:
                    if self._callback:
                        callback()
                    else:
                        print("detected keyword!")

        except Exception as e:
            print(f'error: {e}')



if __name__ == "__main__":
    listener = KeywordDetection()
    listener.run()

