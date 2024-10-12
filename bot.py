from bot_token import TOKEN, IMAGE_POST_URL

from urllib.request import urlretrieve
import telebot
import requests
from telebot import types

PHOTO_DL_URL = "https://api.telegram.org/file/bot" + TOKEN + "/"

IMAGE_LIST_FILE = "image_list.txt"

def get_images_from_filelist(image_text_file):
    try:
        image_list_file = open(image_text_file, 'r')
        image_list = []
        for file in image_list_file.readlines():
            image_list.append( file.replace('\n', '') )
        image_list_file.close()
        return image_list
    except:
        print(FileNotFoundError.strerror())
        image_list_file = open(image_text_file, "w")
        image_list_file.close()
        # image_list_file = open("image_list.txt", 'r')
        return []
    finally:
        # esto lo puedo borrar, pero no quiero.
        pass

def write_last_image(new_image_path):
    image_list = get_images_from_filelist(IMAGE_LIST_FILE)
    
    image_list.insert(0, new_image_path)
    print(image_list.pop())

    list_file = open(IMAGE_LIST_FILE, "w")
    GLOBAL_IMAGE_LIST.clear()
    for photo_path in image_list:
        list_file.writelines(photo_path + '\n')
        GLOBAL_IMAGE_LIST.append(photo_path)
    list_file.close()

GLOBAL_IMAGE_LIST = get_images_from_filelist(IMAGE_LIST_FILE)
for image in GLOBAL_IMAGE_LIST:
    print (image)
#print (GLOBAL_IMAGE_LIST)

bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Lista de comandos con '/'
bot.set_my_commands(
    commands=[
# 2024.10.12 edito comandos
        telebot.types.BotCommand("view_last_photos", "Ver las 3 fotos"),
        telebot.types.BotCommand("donate", "Donar"),
        telebot.types.BotCommand("/view_photo", "Ver la última foto")
    ],
    scope= telebot.types.BotCommandScopeAllPrivateChats()
)

@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.reply_to(message, "Hola, cómo estás?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Enviando ayuda... prueba escribirme o enviar una imágen")

@bot.message_handler(commands=['view_last_photos'])
def send_last_three_photos(message):
#    bot.send_photo(command.message.chat.id, open("download/photos/" + GLOBAL_IMAGE_LIST[1], 'rb'))
    bot.send_photo(message.chat.id, open("download/photos/" + GLOBAL_IMAGE_LIST[1], 'rb'))
#    bot.
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
        if command.data == 'view_photos' or command.data == "/view_photos":
            # enviar las 3 fotos más recientes
            bot.reply_to(command.message, "Entra a https://ramirorios.pythonanywhere.com/ para ver las últimas 3 fotos!")
            # bot.send_message(command.message.chat.id, "TODO: ver 3 fotos.")
            if len(GLOBAL_IMAGE_LIST) > 0:
                bot.send_photo(command.message.chat.id, open("download/photos/" + GLOBAL_IMAGE_LIST[0], 'rb'))
                bot.send_photo(command.message.chat.id, open("download/photos/" + GLOBAL_IMAGE_LIST[1], 'rb'))
                bot.send_photo(command.message.chat.id, open("download/photos/" + GLOBAL_IMAGE_LIST[2], 'rb'))
            else:
                bot.reply_to(command.message, "Aún no hay fotos! Por favor, envíame una foto")
        if command.data == 'view_last_photo':
            # DONE #bot.send_message(command.message.chat.id, "TODO: ver ultima foto..")
            bot.send_message(command.message.chat.id, "La última foto ->")
            bot.send_photo(command.message.chat.id, open("download/photos/" + GLOBAL_IMAGE_LIST[0], 'rb'))
        if command.data == 'donate' or command.data == '/donate':
            bot.send_message(command.message.chat.id, "En Argentina pueden donar en pesos a MercadoPago")
            bot.send_message(command.message.chat.id, "Alias: mimujermedicenerd")
            bot.send_message(command.message.chat.id, "GRACIAS!")
    #pass



@bot.message_handler(content_types=['photo'])
def receive_photo(message):
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
    print (" -DESCARGANDO FOTO photo3-")
    print ( photo3.file_path )
    # Se descarga la foto al directorio de descargas local download/
    urlretrieve(PHOTO_DL_URL + photo3.file_path, "download/" + photo3.file_path)

    bot.reply_to(message, "Oh, una foto! la descargaré")
    bot.send_message(message.chat.id, "Espera por favor...")
    
    # sube la imagen a flask
    url = IMAGE_POST_URL + '/post_image'
    my_photo = {'image': open("download/" + photo3.file_path, 'rb')}
    x = requests.post(url, files=my_photo)
    print(x.json)

    # guarda la imágen en la lista

    photo_dir, photo_file_name = photo3.file_path.split('/')

    write_last_image( photo_file_name)
    print("El dir es ", photo_dir)
    print("El filename es ", photo_file_name)


    bot.send_message(message.chat.id, "Listo! Puedes verla en línea en https://ramirorios.pythonanywhere.com/")
    #bot.send_photo(message.chat.id, message.photo[1].file_id)

    


bot.infinity_polling()
