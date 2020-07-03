import telebot
import scrapper
from pprint import pprint
import os
from flask import Flask

APP_NAME = 'olxxxer'
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт, ти написав мені /start')

@bot.message_handler(content_types=['text'])
def send_text(message):
    adverts = scrapper.search_by_keyword(message.text.lower())
    for advert in adverts:
        bot.send_message(message.chat.id, f'{advert.title}\n\u20B4{advert.price}\n{advert.link}')

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://{APP_NAME}.herokuapp.com/{TOKEN}')
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))