import argparse
from threading import Thread

from pvcheetah import *
from pvrecorder import PvRecorder

import utils


class STT(Thread):
    def __init__(
            self, 
            access_key=None, 
            library_path=None, 
            model_path=None, 
            endpoint_duration_sec=1.
            ):
        super(STT, self).__init__()

        if access_key:
            self._access_key = access_key
        else:
            self._access_key = utils.load_api_key()

        self._library_path = library_path
        self._model_path = model_path
        self._endpoint_duration_sec = endpoint_duration_sec
        self._is_recording = False
        self._stop = False

        self._out = create(
                access_key=self._access_key,
                library_path=self._library_path,
                model_path=self._model_path,
                endpoint_duration_sec=self._endpoint_duration_sec)
        self._recorder = PvRecorder(device_index=-1, frame_length=self._out.frame_length)

    def listen(self):
        recorder = self._recorder
        recorder.start()

        transcribed_text = ""
        while True:
            partial_transcript, is_endpoint = self._out.process(recorder.read())
            transcribed_text += partial_transcript

            if is_endpoint:
                transcribed_text += self._out.flush()
                return transcribed_text.lower()


if __name__ == '__main__':
    STT().listen()
