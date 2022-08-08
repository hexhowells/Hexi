import telebot
import os
from hexi.auth import auth

def get_api_token():
    return auth.keys["telegram"]


class TelegramBot:
    def __init__(self, user_id):
        self.bot = telebot.TeleBot(get_api_token())
        self.user_id = user_id


    def send_message(self, message):
        self.bot.send_message(self.user_id, message)


    def send_image(self, image):
        self.bot.send_photo(self.user_id, image)


    def send_video(self, video):
        self.bot.send_video(self.user_id, video)
