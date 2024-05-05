import telebot
from telebot import types
from currency_converter import CurrencyConverter
bot = telebot.TeleBot('Your API token')

currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Какую сумму вы хотите обменять?')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Напишите сумму для конвертации')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('RUB/CNY', callback_data='rub/cny')
        btn4 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
        btn5 = types.InlineKeyboardButton('Другая пара', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, 'Выберите пару', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получилось: {round(res, 2)}. Можете ввести другую сумму или выбрать другую пару: ')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару валют через слэш(xxx/yyy)')
        bot.register_next_step_handler(call.message, mycurrency)


def mycurrency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получилось: {round(res, 2)}. Можете ввести другую сумму или выбрать другую пару: ')
        bot.register_next_step_handler(message, mycurrency)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то пошло не так! Введите значение заново: ')
        bot.register_next_step_handler(message, mycurrency)


bot.polling(none_stop=True)
