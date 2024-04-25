import telebot
import requests
import json


bot = telebot.TeleBot('Your bot API')

#API сайта
API = '39fe531903d9290ac0b8a56bed5ae58e'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Давай узнаем погоду! Напиши город:')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temperature = data['main']['temp']
        bot.reply_to(message, f'Сейчас погода:{temperature}')
        #Отправляем картинку в зависимости от градусов
        image = 'солнце.png' if temperature > 15 else 'облако.jpg'
        with open(image, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.reply_to(message, 'Город указан не верно!')


#Запускаем бота
bot.polling(none_stop=True)


