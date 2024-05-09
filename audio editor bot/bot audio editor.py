import telebot
from telebot import types
import moviepy.editor


bot = telebot.TeleBot('Your API')


@bot.message_handler(commands=['start'])
def start_bot(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text="Извлечь")
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Привет! Этот бот поможет извлечь аудио дорожку из любого видео', reply_markup=keyboard)
    with open('звуковая дорожка.jpeg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: True)
def handle_button_click(message):
    if message.text == "Извлечь":
        bot.send_message(message.chat.id, 'Отправь файл для извлечения аудиодорожки(в формате mp4)')
    else:
        bot.send_message(message.chat.id, "Нажмите кнопку для продолжения")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    video_clip = moviepy.editor.VideoFileClip(downloaded_file)
    audio_clip = video_clip.audio
    audio_file = audio_clip.write_audiofile('new_audio .mp3')

    with open(audio_file, 'rb') as file:
        bot.send_audio(message.chat.id, file)


bot.polling(none_stop=True)

