import os
import requests
import json
from flask import Flask, request

app = Flask(__name__)

# Токен из переменных среды Render
TOKEN = os.getenv('BOTTOKEN', '')
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return requests.post(url, json=payload)

# ПИШЕМ МАРШРУТЫ ОТДЕЛЬНО И ЯВНО
@app.route('/', methods=['GET', 'POST'])
def root():
    return webhook_logic()

@app.route('/api/index', methods=['GET', 'POST'])
def api_index():
    return webhook_logic()

@app.route('/test', methods=['GET', 'POST'])
def test():
    return webhook_logic()

def webhook_logic():
    # Если зашли через браузер (GET)
    if request.method == 'GET':
        return "🎉 СЕРВЕР РАБОТАЕТ! Теперь Telegram сможет присылать сообщения!", 200
    
    # Если пришло сообщение от Telegram (POST)
    if not TOKEN:
        return "Ошибка: BOTTOKEN не найден", 500

    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return "OK", 200

        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')

        if text == '/start':
            markup = {
                "keyboard": [
                    ["🏙 Купить квартиру", "🏠 Купить дом"],
                    ["📞 Контакты"]
                ],
                "resize_keyboard": True
            }
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
