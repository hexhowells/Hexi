import telebot
from datetime import datetime
import time
import os
from PIL import Image

from hexi.auth import auth
from hexi.config import config
from hexi.interfaces.display import display, icons
from hexi.interfaces.speaker import sound
from hexi.interfaces.motor import Motor
from hexi.interfaces.camera import camera as cam_interface


class HexiTeleBot(telebot.TeleBot):
    def __init__(self, *args, **kwargs):
        self.pause_token = None
        self.debug_on = False
        self.screen = display.Display(font="fontawesome2.ttf")
        super(HexiTeleBot, self).__init__(*args, **kwargs)


bot = HexiTeleBot(auth.keys["telegram"])
all_commands = ['help', 'debug', 'ping', 'motor', 'screen', 'faces', 'camera', "speaker"]



@bot.message_handler(commands=['help'])
def help(message):
    if message.chat.id not in auth.id_whitelist: return
    msg = "--- COMMANDS ---\n"
    msg += '\n'.join(all_commands)
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['ping'])
def ping(message):
    if message.chat.id not in auth.id_whitelist: return
    now_raw = datetime.now()
    now = now_raw.strftime("%d/%m/%Y %H:%M:%S")
    msg = f'ping recieved at {now}'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['debug'])
def debug(message):
    if message.chat.id not in auth.id_whitelist: return

    bot.debug_on = not bot.debug_on
    if bot.debug_on:
        if not bot.pause_token.is_paused():
            bot.pause_token.pause()
            bot.screen.show_icon(icons.Wrench)
    else:
        bot.pause_token.unpause()

    bot.send_message(message.chat.id, f"debug set to {bot.debug_on}")


@bot.message_handler(commands=['motor'])
def motor(message):
    if message.chat.id not in auth.id_whitelist: return
    if not bot.debug_on:
        bot.send_message(message.chat.id, "debug mode is not active")
    else:
        bot.send_message(message.chat.id, "driving motors forward for 1 second")
        motor = Motor()
        motor.drive(Motor.FORWARD, 1)


@bot.message_handler(commands=['screen'])
def screen(message):
    if message.chat.id not in auth.id_whitelist: return
    if not bot.debug_on:
        bot.send_message(message.chat.id, "debug mode is not active")
    else:
        bot.send_message(message.chat.id, "testing all screen pixels")
        screen = display.Display()
        screen.draw_rectangle(0, 0, 64, 128)
        time.sleep(5)
        screen.clear()


@bot.message_handler(commands=['faces'])
def faces(message):
    if message.chat.id not in auth.id_whitelist: return
    if not bot.debug_on:
        bot.send_message(message.chat.id, "debug mode is not active")
    else:
        bot.send_message(message.chat.id, "testing all faces for Hexi")
        screen = display.Display()
        
        assets_path = "/home/pi/Hexi/hexi/assets/face/"
        for file_name in os.listdir(assets_path):
            filetype = file_name.split('.')[-1]
            if filetype != 'png': continue
            
            filepath = assets_path + file_name
            face_image = Image.open(filepath)
            screen.show_image(face_image)
            time.sleep(4)

        screen.clear()


@bot.message_handler(commands=['camera'])
def camera(message):
    if message.chat.id not in auth.id_whitelist: return
    if not bot.debug_on:
        bot.send_message(message.chat.id, "debug mode is not active")
    else:
        bot.send_message(message.chat.id, "captuing image")
        cam = cam_interface.Camera()
        photo_array = cam.capture(delay=1)
        photo_array = photo_array[:,:,::-1]  # convert BGR to RGB
        photo = Image.fromarray(photo_array)   

        bot.send_photo(message.chat.id, photo)

        cam.close()


@bot.message_handler(commands=['speaker'])
def speaker(message):
    if message.chat.id not in auth.id_whitelist: return
    if not bot.debug_on:
        bot.send_message(message.chat.id, "debug mode is not active")
    else:
        bot.send_message(message.chat.id, "playing a tone through the speakers")
        sound.play_wav("/home/pi/Hexi/hexi/assets/audio/sine.wav")

@bot.message_handler(func=lambda message: True)
def recieve_message(message):
    if message.chat.id not in auth.id_whitelist: return
    bot.pause_token.pause()
    bot.screen.show_icon(icons.Envelope)
    print(message.text)

    bot.send_message(message.chat.id, "message recieved!")
    with open("telegram/messages.txt", "w") as msg_file:
        msg_file.write(message.text)



def start_bot(pause_token):
    bot.pause_token = pause_token
    bot.infinity_polling()

