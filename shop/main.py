import telebot
from telebot import types
import sqlite3
import config
import logging


logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(config.TOKEN)
name, age, city, sex, about = None, None, None, None, None


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Регистрация')
    btn2 = types.KeyboardButton('Поиск')
    btn3 = types.KeyboardButton('Посмотреть информацию о себе')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     "Привет. Если ты зашел в первый раз, то давай зарегистрируемся. Если ты уже с нами, то жми поиск",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def registration(message):
    if message.text == 'Регистрация':
        conn = sqlite3.connect('registration.sql')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS registration(id integer auto_increment, user_id integer, name varchar(40), age varchar(40), city varchar(50), sex varchar(10), about text(500))")
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, "Идет твоя регистрация... Введите ваше имя")
        bot.register_next_step_handler(message, add_name)

    elif message.text == 'Посмотреть информацию о себе':
        conn = sqlite3.connect('registration.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM registration')
        users = cur.fetchall()
        info = ' '
        for el in users:
            info += f"name {name}, age {age}/n"
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, info)


def add_name(message):
    name = message.text.strip()
    bot.send_message(message.chat.id, "Введите ваш возраст. Например: 23")
    bot.register_next_step_handler(message, add_age)


def add_age(message):
    try:
        age = message.text.strip()
    except Exception:
        print("Введите корректное значение")
    bot.send_message(message.chat.id, "Введите ваш город")
    bot.register_next_step_handler(message, add_city)


def add_city(message):
    city = message.text.strip()
    bot.send_message(message.chat.id, "Введите ваш пол: мужской или женский")
    bot.register_next_step_handler(message, add_sex)


def add_sex(message):
    sex = message.text.strip()
    bot.send_message(message.chat.id, "Расскажите о себе")
    bot.register_next_step_handler(message, add_about)


def add_about(message):
    about = message.text.strip()
    bot.send_message(message.chat.id, "Спасибо. Пришлите смайлик, который вам нравится")
    bot.register_next_step_handler(message, add_user)


def add_user(message):
    conn = sqlite3.connect('registration.sql')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO registration (name, age, city, sex, about) VALUES ('%s', '%s', '%s', '%s', '%s')"
        % (name, age, city, sex, about)
        )
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Посмотреть информацию о себе')
    btn2 = types.KeyboardButton('Поиск')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Поздрaвляю! Регистрация прошла успешно :)",  reply_markup=markup)


@bot.message_handler(content_types=['text'])
def registration(message):
    if message.text == 'Посмотреть информацию о себе':
        conn = sqlite3.connect('registration.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM registration')
        users = cur.fetchall()
        info = 'ghj,  '
        # for el in users:
        #     info += f"name {name}, age {age}"
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, "info")


bot.polling(none_stop=True)

