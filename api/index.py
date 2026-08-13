import os
import telebot
from flask import Flask, request

# Токен из переменных среды Vercel
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

# САМЫЙ ВАЖНЫЙ МОМЕНТ:
# Добавляем '/api/index', чтобы Vercel не выдавал 404
@app.route(['/', '/api/index', '/test'], methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "БОТ РАБОТАЕТ! Теперь пиши ему в Telegram!", 200
    
    if not TOKEN:
        return "Ошибка: BOTTOKEN не найден в настройках Vercel", 500
    
    try:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run()
