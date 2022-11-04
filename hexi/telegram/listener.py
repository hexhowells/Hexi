import telebot
from datetime import datetime

from hexi.auth import auth
from hexi.config import config
from hexi.interfaces.display import display, icons
from hexi.interfaces.speaker import sound
from hexi.interfaces.motor import Motor
from hexi.interfaces.camera import camera


class HexiTeleBot(telebot.TeleBot):
    def __init__(self, *args, **kwargs):
        self.pause_token = None
        self.debug_on = False
        self.screen = display.Display(font="fontawesome2.ttf")
        super(HexiTeleBot, self).__init__(*args, **kwargs)


bot = HexiTeleBot(auth.keys["telegram"])
all_commands = ['help', 'debug', 'ping']



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

