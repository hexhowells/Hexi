import cv2


class Faces():
    def __init__(self):
        xml_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(xml_file)


    def detect(self, frame):
        return self.face_cascade.detectMultiScale(frame, 1.1, 4)

 
