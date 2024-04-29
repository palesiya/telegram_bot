import telebot
from telebot import types
import sqlite3
from currency_converter import CurrencyConverter


name = None
bot = telebot.TeleBot("6641264816:AAF5RcZurrRKNeOE5ohkGkmypYtoUESP9HE")
amount = 0
currency = CurrencyConverter()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Введите сумму:")
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Введите число")
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='USD/EUR')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='EUR/USD')
        btn3 = types.InlineKeyboardButton('GBP/EUR', callback_data='GBP/EUR')
        btn4 = types.InlineKeyboardButton('EUR/GBP', callback_data='EUR/GBP')
        btn5 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, "Выберите пару валют:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Число должно быть больше 0")
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f"получается {round(res, 3)}. Можете заново вписать сумму")
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Введите пару значений через /")
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f"получается {round(res, 3)}. Можете заново вписать сумму")
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, "Неверный формат")
        bot.register_next_step_handler(message, summa)


bot.polling(none_stop=True)
