import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np

class Camera:
    def __init__(
            self,
            resolution = (640, 480),
            framerate=8,
            rotation=180,
            img_format="bgr"
            ):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.rotation = rotation

        self.channels = 3
        self.img_format = img_format


    def stream(self):
        raw_capture = PiRGBArray(self.camera, size=self.camera.resolution)
        for frame in self.camera.capture_continuous(
                            raw_capture, 
                            format=self.img_format, 
                            use_video_port=True):
            yield frame
            raw_capture.truncate(0)


    def capture(self, delay=3):
        h, w = self.camera.resolution
        image = np.empty((w, h, self.channels), dtype=np.uint8)
        self.camera.start_preview()
        time.sleep(delay)
        self.camera.capture(image, self.img_format)
        self.camera.stop_preview()
        return image


    def close(self):
        self.camera.close()
