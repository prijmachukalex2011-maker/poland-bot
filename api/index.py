import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Токен из переменных среды Vercel
TOKEN = os.getenv('BOTTOKEN', '')
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    """Функция для отправки сообщений через requests"""
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return requests.post(url, json=payload)

@app.route(['/', '/api/index', '/test'], methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "Бот работает на легком движке! Теперь всё будет стабильно!", 200
    
    if not TOKEN:
        return "Ошибка: BOTTOKEN не найден", 500

    try:
        # Получаем данные от Telegram
        data = request.get_json()
        if not data or 'message' not in data:
            return "OK", 200

        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')

        # Логика бота
        if text == '/start':
            # Создаем кнопки в формате JSON (как того требует Telegram API)
            markup = {
                "keyboard": [
                    ["🏙 Купить квартиру", "🏠 Купить дом"],
                    ["📞 Контакты"]
                ],
                "resize_keyboard": True
            }
            import json
            send_message(chat_id, "Добро пожаловать в бот по недвижимости в Польше!", json.dumps(markup))
        
        elif text == '🏙 Купить квартиру':
            send_message(chat_id, "Загружаю список квартир...")
        elif text == '🏠 Купить дом':
            send_message(chat_id, "Загружаю список домов...")
        elif text == '📞 Контакты':
            send_message(chat_id, "Свяжитесь с нами по телефону: +48 XXX XXX XXX")
        else:
            send_message(chat_id, "Я пока не понимаю эту команду.")

        return "OK", 200

    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run()
