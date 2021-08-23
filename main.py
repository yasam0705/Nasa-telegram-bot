import telebot, json, requests
from random import randint
from telebot import types
from telebot.apihelper import ApiException
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TG_TOKEN = os.environ.get('TG_TOKEN')
NASA_TOKEN = os.environ.get('NASA_TOKEN')

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    start_text = """
    Нажмите на кнопку 'Фото дня'\nИли напишите дату в формате YYYY-MM-DD
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Фото дня')
    item2 = types.KeyboardButton('Рандомное фото')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, start_text, reply_markup=markup)


@bot.message_handler()
def text(message):
    year = month = day = 0
    if message.text == 'Фото дня':
        req = requests.get('https://api.nasa.gov/planetary/apod?', {
            "api_key": NASA_TOKEN,
        })
    elif message.text == 'Рандомное фото':
        year = randint(2000, 2021)
        month = randint(1, 12)
        day = randint(1, 30)
        print(f'{year}-{month}-{day}')
        bot.send_message(message.chat.id, f"Date: {year}-{month}-{day}")

        req = requests.get('https://api.nasa.gov/planetary/apod?', {
            "date": f"{year}-{month}-{day}",
            "api_key": NASA_TOKEN,
        })
    else:
        req = requests.get('https://api.nasa.gov/planetary/apod?', {
            "date": f"{message.text}",
            "api_key": NASA_TOKEN,
        })

    print(message)
    response = json.loads(req.text)
    photo = response['url']
    title = response['title']
    # hd_photo = response['hdurl']
    desc = f"*{title}*\n\n{response['explanation']}"
    try:
        bot.send_photo(message.chat.id, photo, caption=desc, parse_mode="Markdown")
    except ApiException:
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, desc, parse_mode="Markdown")
        # bot.send_photo(message.chat.id, photo, caption=desc)


bot.polling()
