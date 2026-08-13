from flask import Flask, request

app = Flask(__name__)

@app.route(['/', '/api/index', '/test'], methods=['GET', 'POST'])
def webhook():
    # 1. Проверка связи (GET запрос)
    if request.method == 'GET':
        return "SERVER IS ALIVE! If you see this, Flask is working!", 200
    
    # 2. Обработка сообщения от Telegram (POST запрос)
    try:
        import os
        import telebot # Импорт только в момент запроса
        
        TOKEN = os.getenv('BOTTOKEN')
        if not TOKEN:
            return "Error: BOTTOKEN not found in Environment Variables", 500
            
        bot = telebot.TeleBot(TOKEN)
        
        # Обработчики команд
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

        # Обработка обновления
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200

    except Exception as e:
        print(f"Bot Error: {str(e)}")
        return f"Internal Bot Error: {str(e)}", 500

if __name__ == "__main__":
    app.run()
