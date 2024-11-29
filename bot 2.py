import time
import telebot
from database import *

TOKEN = "7215372318:AAERp_VM4GbiuxWta6zmnsKMV1nLeN4mmrE"
bot = telebot.TeleBot(TOKEN)
def time_now():
    return time.ctime(time.time())
photo_list = []

@bot.message_handler(commands=['create_database'])
def database(message):
    create_datatable()
    bot.send_message(message.chat.id, 'База данных создана!')


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Приветствую тебя в предложке канала https://t.me/spaseniepostupaushih.')
    bot.send_message(message.chat.id, 'Для того, чтобы предложить новость нажми /new_post')


@bot.message_handler(commands=['new_post'])
def handle_new_post(message):
    user_reg(message.from_user.id)
    bot.send_message(message.chat.id, 'Окей, теперь отправь мне новость. Важно учесть, что если отправленное '
                     'покажется админу неуместным здесь, то он отклонит твою новость, а в крайнем случае ты можешь попасть в бан'
                     'на неделю.')
    bot.send_message(message.chat.id, 'P.S. Если ты хочешь загрузить фото с текстом, то они должны идти одним сообщением, а иначе они '
                     'отправятся некорректно. Важно учесть, что если админ еще не проверил вашу старую новость, а вы уже отправили новую, '
                     'то старая заменится на новую. Вместе с новостью можно загрузить только одно фото, при загрузке большего количества фото будет браться только первое из загруженных.')
    bot.register_next_step_handler(message, up)
    

def up(message):
    file_info = bot.get_file(message.photo[0].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = filepath + message.photo[0].file_id
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    create_new_news(message.from_user.id, message.caption, time_now())
    bot.send_message(message.chat.id, 'Твоя новость получена, как только админ ее проверит, она будет опубликована.')


@bot.message_handler(content_types=['text'])
def otvetka(message):
    bot.send_message(message.chat.id, 'Для того чтобы вернуться в начало бота нажми /start, для предложки нажми /new_post. '
                     'У меня нету альтернативного функционала, кроме предложки для этого канала: '
                     'https://t.me/spaseniepostupaushih. (Если ты хочешь устроить восстание машин нажми сюда /revolution)')
    

bot.polling()