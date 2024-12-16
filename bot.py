import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telebot import types
import openpyxl
import sqlite3
import os

TOKEN = "7892036740:AAHqRp3BDJRq80K1Ld84NIIYTem8nF2QqMA"
bot = telebot.TeleBot(TOKEN)

TOKENTWO = "8043071049:AAFHNnu_eExj9LdYEBPeR1r4TpkRiwhitF4"
botspam = telebot.TeleBot(TOKENTWO)

global photos
global txt
global p
global knpk 
knpk = False
txt = ''
photos = []
p = True
sc = 1
text_on = ""
ssilka = ""


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

# хелп клава для ссылкок
step_s = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yes = types.KeyboardButton('Да')
step_s.add(yes)
no = types.KeyboardButton('Нет')
step_s.add(no)

# Доп клава, для ссылок
ssilki = types.InlineKeyboardMarkup()
knopka_ssilki = types.InlineKeyboardButton(text_on, url=ssilka)
ssilki.add(knopka_ssilki)

@bot.message_handler(commands=['start'])
def handle_start(message):
    txt = ''
    photos = []
    p = True
    bot.send_message(message.chat.id, "Ты будешь добавлять кнопку для ссылки?", reply_markup=step_s)
    bot.register_next_step_handler(message, proverka_knopki)

def proverka_knopki(message):
    if message.text == 'Да':
        global knpk
        knpk = True
        bot.send_message(message.chat.id, "Введите текст, который будет на кнопке")
        bot.register_next_step_handler(message, knopka_step1)
    else:
        global ssilki
        ssilki = ""
        global text_on
        text_on = ""
        texxt(message)

def knopka_step1(message):
    global text_on
    text_on = message.text
    bot.send_message(message.chat.id, "Теперь отправь мне ссылку, которая будет внутри кнопки")
    bot.register_next_step_handler(message, knopka_step2)

def knopka_step2(message):
    global ssilka
    ssilka = message.text
    bot.send_message(message.chat.id, "Отлично, кнопка добавлена")
    texxt(message)

def texxt(message):
    bot.send_message(message.chat.id, 'Отправь мне текст рассылки. ')
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

def path():
    dire = os.path.abspath(__file__)
    s = ""
    t = False
    for i in range(len(dire)-1, -1, -1):
        if t:
            s = dire[i] + s
        if dire[i] == '/':
            t = True
    return s

def step3(message):
    global sc
    try:
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        s = path()
        save_path = f'{s}/img/{sc}.jpg'
        photos.append(save_path)
    except:
        video = message.video
        file_info = bot.get_file(video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        s = path()
        save_path = f'{s}/img/{sc}.mp4'
        photos.append(save_path)
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    sc += 1
        
    bot.send_message(message.chat.id, "Медиа добавлено, если нужно добавить еще, просто отправь мне медиа, иначе нажми на кнопку", reply_markup=no_keyboard)
    bot.register_next_step_handler(message, step35)
        
        

def step35(message):
    if message.text == "Перейти к следующему шагу":
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
    sss = []
    ssilki = types.InlineKeyboardMarkup()
    knopka_ssilki = types.InlineKeyboardButton(text_on, url=ssilka)
    ssilki.add(knopka_ssilki)
    for photo in photos:
        if '.jpg' in photo:
            sss.append(telebot.types.InputMediaPhoto(open(photo, 'rb'), caption=txt))
        else:
            sss.append(telebot.types.InputMediaVideo(open(photo, 'rb'), caption=txt))
    try:
        if knpk:
            if not p: 
                bot.send_message(message.chat.id, txt, reply_markup=ssilki)
            else:
                bot.send_media_group(message.chat.id, sss, reply_markup=ssilki)
        else:
            if not p: 
                bot.send_message(message.chat.id, txt)
            else:
                bot.send_media_group(message.chat.id, sss)
    except:
        print(-1)
        bot.send_message(message.chat.id, "Вы указали некорректную ссылку в кнопке, давайте начнем сначала")
        handle_start(message)
    bot.send_message(message.chat.id, "Такое сообщение будет отправлено. Если вы согласны, то нажмите Да, иначе Нет", reply_markup=step_s)
    bot.register_next_step_handler(message, step6)


def step6(message):
    if message.text == 'Да':
        ssilki = types.InlineKeyboardMarkup()
        knopka_ssilki = types.InlineKeyboardButton(text_on, url=ssilka)
        ssilki.add(knopka_ssilki)
        bot.send_message(message.chat.id, "Начинаю отправку пользователям")
        global p
        lost = 0
        nice = 0
        conn = sqlite3.connect('../chatgpt_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT tid FROM Users")
        massive_big = cursor.fetchall()
        sss = []
        no_send = []
        for photo in photos:
            if '.jpg' in photo:
                sss.append(telebot.types.InputMediaPhoto(open(photo, 'rb'), caption=txt))
            else:
                sss.append(telebot.types.InputMediaVideo(open(photo, 'rb'), caption=txt))
        for z in range(len(massive_big)):
            try:
                if knpk:
                    if not p: 
                        botspam.send_message(massive_big[z][0], txt, reply_markup=ssilki)
                    else:
                        botspam.send_media_group(massive_big[z][0], sss, reply_markup=ssilki)
                else:
                    if not p: 
                        botspam.send_message(massive_big[z][0], txt)
                    else:
                        botspam.send_media_group(massive_big[z][0], sss)
                nice += 1
            except:
                no_send.append(massive_big[z][0])
                lost += 1
        for i in range(1, 4):
            for x in no_send:
                try:
                    if knpk:
                        if not p: 
                            botspam.send_message(massive_big[z][0], txt, reply_markup=ssilki)
                        else:
                            botspam.send_media_group(massive_big[z][0], sss, reply_markup=ssilki)
                    else:
                        if not p: 
                            botspam.send_message(massive_big[z][0], txt)
                        else:
                            botspam.send_media_group(massive_big[z][0], sss)
                    lost -= 1
                    nice += 1
                    no_send.remove(x)
                except:
                    print(-1)
            
        p = True
        knpk = False
        bot.send_message(message.chat.id, "Отправка окончена:")#telebot.types.InputMediaVideo(open(photo, 'rb'), caption=txt)
        bot.send_message(message.chat.id, f"lost requests: {lost}\nnice requestes: {nice}")
        bot.send_message(message.chat.id, "/start to start new malling") 
    else:
        knpk = False
        txt = ''
        photos = []
        p = True
        sc = 1
        text_on = ""
        ssilka = ""
        handle_start(message)



bot.polling()
