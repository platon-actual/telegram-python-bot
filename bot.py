from bot_token import TOKEN
import telebot

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.reply_to(message, "Hola, cómo estás?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Enviando ayuda... (pruebe con /start, /help o escriba un mensaje)")

@bot.message_handler(func= lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()