# import interfaces here
from hexi.telegram import telegram
from hexi.interfaces.camera import camera
from hexi.interfaces.display import display, icons
from PIL import Image
import time


# entry point of skill
def start(command=None):
    bot = telegram.TelegramBot(5578693112)
    cam = camera.Camera()
    screen = display.Display()

    # countdown
    for i in range(3, 0, -1):
        screen.draw_text_custom(str(i), 50, 18, size=38)
        time.sleep(1)
        screen.clear()

    screen.show_icon(icons.Camera)
    photo_array = cam.capture(delay=1)
    photo = Image.fromarray(photo_array)

    bot.send_image(photo)

    screen.clear()



if __name__ == "__main__":
    start()
