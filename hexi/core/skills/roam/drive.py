#from floor import Floor
import cv2
import numpy as np
import time
import random

from hexi.features.floor import Floor
from hexi.interfaces.motor import Motor


class Drive:
    def __init__(self):
        self.floor_model = Floor()
        self.action_map = {0: Motor.LEFT, 1: Motor.FORWARD,
                           2: Motor.RIGHT, 3: Motor.BACKWARD}

    
    def compute_path(self, image):
        floor = self._get_floor(image)
        action, action_len = self._get_action(floor)

        return action, action_len


    def _get_floor(self, image):
        small_img = self.floor_model.downsample(image)
        
        coords = self.floor_model.segment_floor(small_img)
        heights = [480-a[1] for a, b in coords]
        
        # clip heights
        heights = [min(self.floor_model.height//2, x) for x in heights]
        
        # split map into 3 buckets
        h_buckets = []
        
        step = 20
        for i in range(step, 61, step):
            avg_h = sum(heights[i-step:i]) / step
            h_buckets.append(avg_h)
        
        return h_buckets


    def _get_action(self, h_buckets):
        if sum(h_buckets) == 0:
            return self.action_map[3], 1
        else:
            p = softmax(h_buckets)
            sample = list(np.random.multinomial(10, p))
            action_idx = sample.index(max(sample))

        if action_idx == 1:
            return self.action_map[action_idx], 2
        else:
            return self.action_map[action_idx], random.choice([0.1, 0.2, 0.3, 0.4, 0.5])



def softmax(x):
    x = np.array(x)
    return x / np.sum(x)

