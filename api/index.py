import os
import requests
import json
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv('BOTTOKEN', '').strip()
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return requests.post(url, json=payload)

# Добавляем /webhook как основной путь
@app.route('/webhook', methods=['POST'])
def webhook():
    if not TOKEN:
        return "Error: BOTTOKEN missing", 500
    try:
        raw_data = request.data.decode('utf-8')
        data = json.loads(raw_data)
        print("--- СООБЩЕНИЕ ПРИШЛО НА /webhook! ---")
        
        if 'message' not in data:
            return "OK", 200

        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '').strip()

        if text == '/start':
            markup = {"keyboard": [["🏙 Купить квартиру", "🏠 Купить дом"], ["📞 Контакты"]], "resize_keyboard": True}
            send_message(chat_id, "Добро пожаловать в бот по недвижимости в Польше! 🇵🇱", json.dumps(markup))
        elif text == '🏙 Купить квартиру':
            send_message(chat_id, "🔎 Загружаю список квартир...")
        elif text == '🏠 Купить дом':
            send_//message(chat_id, "🔎 Загружаю список домов...")
        elif text == '📞 Контакты':
            send_message(chat_id, "📲 Контакты: +48 XXX XXX XXX")
        else:
            send_message(chat_id, f"Я пока не знаю команду '{text}'")

        return "OK", 200
    except Exception as e:
        print(f"Error: {e}")
        return "OK", 200 # Всегда отвечаем OK, чтобы Telegram не ругался

@app.route('/')
def home():
    return "Бот работает! Перенаправьте вебхук на /webhook", 200

if __name__ == "__main__":
    app.run()
