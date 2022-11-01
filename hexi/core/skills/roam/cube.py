from hexi.features.fiducial import find_marker
from hexi.interfaces.motor import Motor


class FindCube:
    def __init__(self):
        self.center_x = 320
        self.tolerance = 50

    def find(self, image):
        
        marker_points, marker_sizes = find_marker(image)

        if len(marker_points) > 0:
            cX, _ = marker_points[0]
            m_size = marker_sizes[0]

            tolerance = 50 if m_size < 65 else 80

            if m_size > 280:
                return True, None, -1

            if cX < (self.center_x - tolerance):
                return True, Motor.LEFT, 0.05
            elif cX > (self.center_x + tolerance):            
                return True, Motor.RIGHT, 0.05
            else:
                return True, Motor.FORWARD, 0.3
        else:
            return False, None, -1


