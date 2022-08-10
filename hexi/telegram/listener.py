import telebot
from hexi.auth import auth


bot = telebot.TeleBot(auth.keys["telegram"])


# initial setup of user
# check first if current user id exists
@bot.message_handler(commands=['start'])
def setup_user(message):
    pass


@bot.message_handler(commands=['wifi'])
def wifi_setup(message):
    pass


# recieve incoming messages
# if message not from main user then store for user viewing
@bot.message_handler(func=lambda message: True)
def recieve_message(message):
    pass
