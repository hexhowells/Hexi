from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from luma.core.virtual import viewport

import inspect


assets_folder = "../../assets/"


class Display:
    def __init__(self, port=1, address=0x3C):
        self.device = sh1106(i2c(port=port, address=address))
        self.height = self.device.height
        self.width = self.device.width
        self.virtual = viewport(self.device, width=self.width, height=self.height)
        self.mode = self.device.mode


    def set_constrast(self, level):
        assert 0 <= level <= 255, "contrast must be between 0-255"
        
        self.device.constrast(level)


    def show_image(self, img, x=0, y=0, fill="white"):
        with canvas(self.virtual) as draw:
            draw.bitmap((x,y), img, fill=fill)


    def show_text(self, text, x=0, y=0):
        assert 0 <= x <= 128, "x position should be between 0-128"
        assert 0 <= y <= 64, "y position should be between 0-128"

        with canvas(self.virtual) as draw:
            draw.text((x,y), text, fill="white")
            print(inspect.signature(draw.text))

