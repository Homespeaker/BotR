import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telebot import types
import openpyxl
import sqlite3

TOKEN = "7892036740:AAHqRp3BDJRq80K1Ld84NIIYTem8nF2QqMA"
bot = telebot.TeleBot(TOKEN)

TOKENTWO = "8043071049:AAFHNnu_eExj9LdYEBPeR1r4TpkRiwhitF4"
botspam = telebot.TeleBot(TOKENTWO)

global photos
global txt
global p
txt = ''
photos = []
p = True
sc = 1



#Клава step2
step2_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
photo_button = types.KeyboardButton('Добавить медиа')
step2_keyboard.add(photo_button)
text_button = types.KeyboardButton('Изменить текст')
step2_keyboard.add(text_button)
no_photo_button = types.KeyboardButton('Не добавлять медиа')
step2_keyboard.add(no_photo_button)


# Без клавиатуры
no_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
n_photo_button = types.KeyboardButton('Перейти к следующему шагу')
no_keyboard.add(n_photo_button)

@bot.message_handler(commands=['start'])
def handle_start(message):
    txt = ''
    photos = []
    p = True
    bot.send_message(message.chat.id, 'Начинаем рассылку, отправь мне текст рассылки. ')
    bot.register_next_step_handler(message, step2)

def step2(message):
    global txt
    txt = message.text
    bot.send_message(message.chat.id, f"<pre language='txt'>{txt}</pre>", parse_mode='HTML')
    bot.send_message(message.chat.id, 'Проверь текст, если все нормально, то ты можешь загрузить несколько фото или видео.\nПри загрузке видео учти, что оно должно быть менее 50мб и находиться в формате .mp4!', reply_markup=step2_keyboard)
    bot.register_next_step_handler(message, step25)

def step25(message):
    global p
    if message.text == 'Изменить текст':
        bot.send_message(message.chat.id, "Введи новый текст")
        bot.register_next_step_handler(message, step2)
    elif message.text == 'Добавить медиа':
        bot.send_message(message.chat.id, "Отправляй по одному медиа, как только медиа закончатся, нажми на кнопку и мы перейдем к следующему шагу")
        bot.register_next_step_handler(message, step3)
    elif message.text == 'Не добавлять медиа':
        bot.send_message(message.chat.id, "Пропускаю ввод медиа...")
        bot.send_message(message.chat.id, "Начинаю отправку пользователям")
        p = False
        step5(message)



def step3(message):
    global sc
    try:
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        save_path = f'BotR/img/{sc}' + '.jpg'
        photos.append(save_path)
    except:
        video = message.video
        file_info = bot.get_file(video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        save_path = f'BotR/img/{sc}' + '.mp4'
        photos.append(save_path)
    sc += 1
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
        
    bot.send_message(message.chat.id, "Медиа добавлено, если нужно добавить еще, просто отправь мне медиа, иначе нажми на кнопку", reply_markup=no_keyboard)
    bot.register_next_step_handler(message, step35)
        
        

def step35(message):
    if message.text == "Перейти к следующему шагу":
        bot.send_message(message.chat.id, "Начинаю отправку пользователям")
        step5(message)
    else:
        step3(message)


def step4(message):
    try:
        global table_name
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        if ".xlsx" in file_info.file_path:
            src = 'tables/' + str(message.from_user.id) + '.xlsx'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Таблица сохранена")
            bot.send_message(message.chat.id, "Начинаю отправку пользователям")
            step5(message)
        else:
            bot.send_message(message.chat.id, "Таблица должна быть в формате .xlsx, иначе не принимается. Отправь таблицу в нужном формате.")
            bot.register_next_step_handler(message, step4)
    except:
        bot.send_message(message.chat.id, "Таблица должна быть в формате .xlsx, иначе не принимается. Отправь таблицу в нужном формате.")
        bot.register_next_step_handler(message, step4)


def step5(message):
    global p
    conn = sqlite3.connect('chatgpt_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT tid FROM Users")
    massive_big = cursor.fetchall()#этот метод вернет вам все элементы в одном кортеже. Данные из строк будут представлены как вложенные кортежи
    #перебираем кортеж с кортежами внутри, также печатаем элементы
    sss = [   ]
    sss = []
    for photo in photos:
        if '.jpg' in photo:
            sss.append(telebot.types.InputMediaPhoto(open(photo, 'rb'), caption=txt))
        else:
            sss.append(telebot.types.InputMediaVideo(open(photo, 'rb'), caption=txt))
    for z in range(len(massive_big)):
        # try:
            if not p: 
                botspam.send_message(massive_big[z][0], txt)
            else:
                botspam.send_media_group(massive_big[z][0], sss)
        # except:
        #     print(-1)
    p = True
    bot.send_message(message.chat.id, "Отправка окончена, для новой рассылки нажми /start")#telebot.types.InputMediaVideo(open(photo, 'rb'), caption=txt)
    



bot.polling()