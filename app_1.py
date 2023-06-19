
import telebot
from telebot import types
from config_1 import exchange, TOKEN
from utils_1 import CurrencyConverter, ConvertionException


def create_markup(hid=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons = []
    for curr in exchange.keys():
        if curr != hid:
            buttons.append(types.KeyboardButton(curr.lower()))
    markup.add(*buttons)
    return markup


def commands_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons = ['/convert', '/values', '/help']
    markup.add(*buttons)
    return markup


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Вы можете вводить валюты с помощью клавиатуры, либо вручную.\n' \
           'Порядок ручного ввода (через пробел) следующий:\n' \
           '<из какой валюты перевести>\n' \
           '<в какую валюту перевести>\n' \
           '<количество переводимой валюты>\n' \
           'Для начала конвертации валют с помощью клавиатуры, введите команду: /convert\n' \
           'Посмотреть список доступных валют: /values\n'

    bot.send_message(message.chat.id, text, reply_markup=commands_markup())


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchange.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text, reply_markup=commands_markup())


@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):
    text = 'Выберете валюту из которой конвертировать:'
    bot.reply_to(message, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, from_handler)


def from_handler(message: telebot.types.Message):
    curr_from = message.text
    text = 'Выберете валюту в которую конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=create_markup(hid=curr_from))
    bot.register_next_step_handler(message, to_handler, curr_from)


def to_handler(message: telebot.types.Message, curr_from):
    curr_to = message.text
    text = 'Напишите количество конвертируемой валюты:'
    bot.send_message(message.chat.id, text, reply_markup=commands_markup())
    bot.register_next_step_handler(message, amount_handler, curr_from, curr_to)


def amount_handler(message: telebot.types.Message, curr_from, curr_to):
    amount = message.text.strip()
    try:
        conv = CurrencyConverter.get_convert(curr_from, curr_to, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка в конвертации:\n{e}')
    else:
        text = f'Стоимость {amount} {curr_from} в {curr_to}:\n{amount}' \
               f' ({exchange[curr_from]}) = {conv} ({exchange[curr_to]})'
        bot.send_message(message.chat.id, text, reply_markup=commands_markup())


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split()
        curr_from, curr_to, amount = values
    except ValueError:
        bot.reply_to(message, 'Неверное количество параметров!\n'
                              'Нажмите /help. Или воспользуйся командой /convert.')
    else:
        curr_from = curr_from.lower()
        curr_to = curr_to.lower()
        try:
            conv = CurrencyConverter.get_convert(curr_from, curr_to, amount)
            text = f'Стоимость {amount} {curr_from} в {curr_to}:\n{amount}' \
                f' ({exchange[curr_from]}) = {conv} ({exchange[curr_to]})'
            bot.send_message(message.chat.id, text, reply_markup=commands_markup())

        except ConvertionException as e:
            bot.reply_to(message, f'Ошибка пользователя\n{e}')
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду\n{e}\n'
                                  f'Нажмите /help. Или воспользуйся командой /convert.')


bot.polling()
