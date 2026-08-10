import os
from flask import Flask, request
import telebot

# 1. Получаем токен из переменных окружения Vercel
TOKEN = "8891147516:AAE5pZOd0nYZNr-bkNur1_pxKPQLO6BDWpw"
bot = telebot.TeleBot(TOKEN)

# ИСПРАВЛЕНО: __name__ вместо name
app = Flask(__name__)

# --- ОБРАБОТЧИКИ ТЕЛЕГРАМ ---

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот для недвижимости в Польше успешно запущен и работает на Vercel!")

# Обработка любых других текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Получено ваше сообщение: {message.text}")

# --- МАРШРУТЫ FLASK ---

# ИСПРАВЛЕНО: Теперь маршрут просто '/', чтобы совпадал с твоей ссылкой Webhook
@app.route('/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
    return "OK", 200

# Страница-заглушка для проверки работы сайта в браузере
@app.route('/test')
def index():
    return "Bot is running! Use /test to check this page."

# ИСПРАВЛЕНО: __name__ == '__main__'
if __name__ == '__main__':
    app.run()

