import telebot
from hexi.auth import auth
from hexi.config import config
from datetime import datetime


bot = telebot.TeleBot(auth.keys["telegram"])


# initial setup of user
# check first if current user id exists
#@bot.message_handler(commands=['start'])
#def setup_user(message):
#    pass



@bot.message_handler(commands=['ping'])
def ping(message):
    now_raw = datetime.now()
    now = now_raw.strftime("%d/%m/%Y %H:%M:%S")
    msg = f'ping recieved at {now}'
    bot.send_message(message.chat.id, msg)



@bot.message_handler(commands=['blackout'])
def blackout(message):
    config_data = config.load()
    config_data['blackout'] = not config_data['blackout']
    config.save(config_data)
    bot.send_message(message.chat.id, f'set blackout mode to {config_data["blackout"]}')



# recieve incoming messages
# if message not from main user then store for user viewing
@bot.message_handler(func=lambda message: True)
def recieve_message(message):
    print("message recieved")
    with open("messages.txt", "a") as msgfile:
        msgfile.write(message.text + "\t\t")


bot.infinity_polling()

