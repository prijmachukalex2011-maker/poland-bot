import os
import telebot
from flask import Flask, request

# Получаем токен. Если он не найден, ставим пустую строку, чтобы бот не 'упал' при запуске
TOKEN = os.getenv('BOTTOKEN', '') 
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🏙 Купить квартиру', '🏠 Купить дом', '📞 Контакты')
    bot.send_message(message.chat.id, "Добро пожаловать в бот по недвижимости в Польше!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == '🏙 Купить квартиру':
        bot.send_message(message.chat.id, "Загружаю список квартир...")
    elif message.text == '🏠 Купить дом':
        bot.send_message(message.chat.id, "Загружаю список домов...")
    elif message.text == '📞 Контакты':
        bot.send_message(message.chat.id, "Свяжитесь с нами по телефону: +48 XXX XXX XXX")
    else:
        bot.send_message(message.chat.id, "Я пока не понимаю эту команду.")

# ИСПРАВЛЕННЫЙ МАРШРУТ: принимаем запросы и на / и на /api/index
@app.route(['/', '/api/index'], methods=['POST'])
def webhook():
    if not TOKEN:
        return "Token not found", 500
    
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/test')
def test():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run()
