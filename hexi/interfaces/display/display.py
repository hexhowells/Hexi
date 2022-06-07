from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from luma.core.virtual import viewport


assets_folder = "../../assets/"


class Display:
    def __init__(self, port=1, address=0x3C):
        self.device = sh1106(i2c(port=port, address=address))
        self.height = self.device.height
        self.width = self.device.width
        self.virtual = viewport(self.device, width=self.width, height=self.height)
        self.mode = self.device.mode


    def show_image(self, img, x=0, y=0, fill="white"):
        with canvas(self.virtual) as draw:
            draw.bitmap((x,y), img, fill=fill)


    def set_background(self, img):
        background = Image.new("RGB", (self.height, self.width), "white")
        background.paste(img)
        self.device.display(background.convert(self.mode))
