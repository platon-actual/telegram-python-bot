from bot_token import TOKEN

from urllib.request import urlretrieve
import telebot

PHOTO_DL_URL = "https://api.telegram.org/file/bot" + TOKEN + "/"

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

@bot.message_handler(content_types=['photo'])
def send_same_photo(message):
    print ("QUE ES ESTO??")
    #for photo_x in message.photo:
    #    print (photo_x.file_id)
    #print (bot.get_file(message.photo[0].file_id))
    photo1 = bot.get_file(message.photo[0].file_id)
    photo2 = bot.get_file(message.photo[1].file_id)
    photo3 = bot.get_file(message.photo[2].file_id)
    print (photo1)
    print (photo2)
    print (photo3)
    urlretrieve(PHOTO_DL_URL + photo2.file_path, "download/" + photo2.file_path)

    bot.reply_to(message, "Oh, una foto! Aún no sé usarla...")
    bot.send_photo(message.chat.id, message.photo[1].file_id)

bot.infinity_polling()