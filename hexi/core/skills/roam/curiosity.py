from hexi.features.image_diff import new_object


class NewObject:
    def __init__(self):
        self.prev_frame = None


    def detect(self, image):
        object_detected = False

        if self.prev_frame is not None:
            object_detected = new_object(self.prev_frame, image)
        
        self.update_prev(image)

        return True if object_detected else False


    def update_prev(self, image):
        self.prev_frame = image

