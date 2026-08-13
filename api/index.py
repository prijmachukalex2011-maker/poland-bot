import os
from flask import Flask, request

# Импортируем telebot внутри функции, чтобы сервер не падал при запуске
app = Flask(__name__)

@app.route(['/', '/api/index', '/test'], methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "Server is ALIVE! If you see this, the server is working.", 200
    
    try:
        import telebot
        # Берем токен из переменных окружения
        TOKEN = os.getenv('BOTTOKEN')
        if not TOKEN:
            return "Error: BOTTOKEN environment variable is missing!", 500
        
        bot = telebot.TeleBot(TOKEN)
        
        # Логика обработки сообщений (перенесена внутрь для стабильности)
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        
        # Создаем обработчики прямо здесь
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

        bot.process_new_updates([update])
        return "OK", 200

    except Exception as e:
        # Если произошла любая ошибка, сервер не упадет, а напишет её в логах
        print(f"CRITICAL ERROR: {e}")
        return f"Bot Error: {str(e)}", 500

if __name__ == "__main__":
    app.run()
