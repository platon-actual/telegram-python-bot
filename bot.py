from bot_token import TOKEN, IMAGE_POST_URL

from urllib.request import urlretrieve
import telebot
import requests
from telebot import types

PHOTO_DL_URL = "https://api.telegram.org/file/bot" + TOKEN + "/"

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.reply_to(message, "Hola, cómo estás?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Enviando ayuda... prueba escribirme o enviar una imágen")

@bot.message_handler(func= lambda m: True)
def echo_all(message):
    # un teclado de opciones:
    markup_keyb = types.InlineKeyboardMarkup(row_width=2)
    
    view_photos_button = types.InlineKeyboardButton("Ver las últimas 3 fotos", callback_data='view_photos')
    view_last_photo_button = types.InlineKeyboardButton("Ver la última foto", callback_data='view_last_photo')
    donate = types.InlineKeyboardButton("Donar a este proyecto!", callback_data='donate')
    #view_photos_button = types.InlineKeyboardButton("Ver las últimas 3 fotos", callback_data='view_photos')

    markup_keyb.add(view_photos_button, view_last_photo_button, donate)
    
    #bot.reply_to(message, "Entra a https://ramirorios.pythonanywhere.com/ para ver las últimas 3 fotos!")
    bot.reply_to(message, message.text + '. Quieres ver las últimas 3 fotos? Puedes enviarme una foto', reply_markup=markup_keyb)
    

@bot.callback_query_handler(func= lambda m: True)
def send_last_photos(command):
    if command.message:
        if command.data == 'view_photos':
            # enviar las 3 fotos más recientes
            bot.reply_to(command.message, "Entra a https://ramirorios.pythonanywhere.com/ para ver las últimas 3 fotos!")
            bot.send_message(command.message.chat.id, "TODO: ver 3 fotos.")
        if command.data == 'view_last_photo':
            bot.send_message(command.message.chat.id, "TODO: ver ultima foto..")
        if command.data == 'donate':
            bot.send_message(command.message.chat.id, "GRACIAS!!!!")
    #pass

@bot.message_handler(content_types=['photo'])
def send_same_photo(message):
    #for photo_x in message.photo:
    #    print (photo_x.file_id)
    #print (bot.get_file(message.photo[0].file_id))
    #photo1 = bot.get_file(message.photo[0].file_id)
    #photo2 = bot.get_file(message.photo[1].file_id)
    photo3 = bot.get_file(message.photo[2].file_id)
    if not photo3:
        bot.send_message(message.chat.id, "La foto es muy pequeña... Prueba con una foto más grande")
        return False
    #print (photo1)
    #print (photo2)
    print (photo3)
    urlretrieve(PHOTO_DL_URL + photo3.file_path, "download/" + photo3.file_path)

    bot.reply_to(message, "Oh, una foto! la descargaré")
    bot.send_message(message.chat.id, "puede verla en línea en https://ramirorios.pythonanywhere.com/")
    #bot.send_photo(message.chat.id, message.photo[1].file_id)

    url = IMAGE_POST_URL + '/post_image'
    my_photo = {'image': open("download/" + photo3.file_path, 'rb')}
    x = requests.post(url, files=my_photo)
    print(x.json)


bot.infinity_polling()