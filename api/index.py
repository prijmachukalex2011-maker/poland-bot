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
    try:
        return requests.post(url, json=payload, timeout=10)
    except:
        return None

# ЭТОТ МАРШРУТ ЛОВИТ ВСЁ (И / , И /test, И /webhook)
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path=''):
    if request.method == 'GET':
        return f"✅ СЕРВЕР ЖИВ! Запрос пришел на адрес: /{path}. Теперь пиши боту в Telegram!", 200
    
    if not TOKEN:
        return "Ошибка: BOTTOKEN не найден", 500

    try:
        # Читаем данные вручную, чтобы избежать ошибок 400/415
        raw_data = request.data.decode('utf-8')
        if not raw_data:
            return "OK", 200
            
        data = json.loads(raw_data)
        
        if 'message' not in data:
            return "OK", 200

        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '').strip()

        if text == '/start':
            markup = {
                "keyboard": [["🏙 Купить квартиру", "🏠 Купить дом"], ["📞 Контакты"]],
                "resize_keyboard": True
            }
            send_message(chat_id, "Добро пожаловать в бот по недвижимости в Польше! 🇵🇱", json.dumps(markup))
        elif text == '🏙 Купить квартиру':
            send_message(chat_id, "🔎 Загружаю список квартир...")
        elif text == '🏠 Купить дом':
            send_message(chat_id, "🔎 Загружаю список домов...")
        elif text == '📞 Контакты':
            send_message(chat_id, "📲 Контакты: +48 XXX XXX XXX")
        else:
            send_message(chat_id, f"Я пока не знаю команду '{text}'")

        return "OK", 200
    except Exception as e:
        print(f"Error: {e}")
        return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
