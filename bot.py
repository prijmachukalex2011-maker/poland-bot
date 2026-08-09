import os
from flask import Flask, request
import telebot

# Получаем токен из переменных окружения Vercel
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот для недвижимости в Польше успешно запущен и работает на Vercel!")

# Обработка любых других текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Получено ваше сообщение: {message.text}")

# Главный маршрут, который принимает запросы от Telegram
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# Страница-заглушка для проверки работы сайта
@app.route('/')
def index():
    return "Bot is running!"

if name == '__main__':
    app.run()
