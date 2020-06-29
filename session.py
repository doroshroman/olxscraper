import telebot
import scrapper
from pprint import pprint
import os

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт, ти написав мені /start')

@bot.message_handler(content_types=['text'])
def send_text(message):
    adverts = scrapper.search_by_keyword(message.text.lower())
    for advert in adverts:
        bot.send_message(message.chat.id, f'{advert.title}\n\u20B4{advert.price}\n{advert.link}')


bot.polling()