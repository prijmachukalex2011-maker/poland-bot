import os
import telebot
from flask import Flask, request

# Токен берется из настроек Vercel (Environment Variables), а не из кода!
TOKEN = os.getenv('BOTTOKEN') 
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    # Пример меню для недвижимости
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🏙 Купить квартиру', '🏠 Купить дом', '📞 Контакты')
    bot.send_message(message.chat.id, "Добро пожаловать в бот по недвижимости в Польше!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == '🏙 Купить квартиру':
        bot.send_message(message.chat.id, "Загружаю список квартир...")
    else:
        bot.send_message(message.chat.id, "Я пока не понимаю эту команду.")

@app.route(['/', '/api/index'], methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/test')
def test():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run()
