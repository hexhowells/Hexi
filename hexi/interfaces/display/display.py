from PIL import Image, ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from luma.core.virtual import viewport, terminal


assets_folder = "../../assets/"


class Display:
    def __init__(self, port=1, address=0x3C):
        self.device = sh1106(i2c(port=port, address=address))
        self.height = self.device.height
        self.width = self.device.width
        self.virtual = viewport(self.device, width=self.width, height=self.height)
        self.mode = self.device.mode
    
    
    def clear(self):
        self.device.clear()


    def set_contrast(self, level):
        assert 0 <= level <= 255, "contrast must be between 0-255"
        
        self.device.contrast(level)


    def show_image(self, img, x=0, y=0, fill="white"):
        with canvas(self.virtual) as draw:
            draw.bitmap((x,y), img, fill=fill)


    def draw_text(self, text, x=0, y=0):
        assert 0 <= x <= 128, "x position should be between 0-128"
        assert 0 <= y <= 64, "y position should be between 0-128"

        with canvas(self.virtual) as draw:
            draw.text((x,y), text, fill="white")


    def draw_pixel(self, x, y, fill="white"):
        with canvas(self.virtual) as draw:
            draw.point((x, y), fill=fill)


    def draw_pixels(self, pixels, fill="white"):
        with canvas(self.virtual) as draw:
            for (x,y) in pixels:
                draw.point((x,y), fill=fill)


    def draw_rectangle(self, x, y, height, width, fill="white", outline="white"):
        with canvas(self.virtual) as draw:
            draw.rectangle((x, y, x+width-1, y+height-1), fill=fill, outline=outline)


    def draw_rectangles(self, rectangles, fill="white", outline="white"):
        with canvas(self.virtual) as draw:
            for (x, y, h, w) in rectangles:
                draw.rectangle((x, y, x+w-1, y+h-1), fill=fill, outline=outline)


class Terminal:
    def __init__(self, display):
        font = ImageFont.truetype("../../assets/fonts/ProggyTiny.ttf", 16)
        self.terminal = terminal(display.device, font)


    def print(self, text):
        self.terminal.animate = False
        self.terminal.puts(text)
        self.terminal.animate = True


    def println(self, text):
        self.terminal.animate = False
        self.terminal.println(text)
        self.terminal.animate = True


    def type(self, text):
        self.terminal.puts(text)


    def typeln(self, text):
        self.terminal.println(text)


    def clear(self):
        self.terminal.clear()


    def flush(self):
        self.terminal.flush()

    
    def backspace(self):
        self.terminal.backspace()

