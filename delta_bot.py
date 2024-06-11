import telebot
from kb import *
from callbacks import callbacks
from config_parser import get_from_global_config
from setting import BOT_TOKEN

token = get_from_global_config(BOT_TOKEN)
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.from_user.id, text = 'Главное меню:', reply_markup=start_kb())


@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    callbacks.get(query.data)(bot, query)

try:
    bot.polling()

except Exception as e:
    print(e)