import os
import requests
import json
import logging
from flask import Flask, request

# Настройка логирования, чтобы видеть всё в консоли Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Токен берем из переменных среды Render
TOKEN = os.getenv('BOTTOKEN', '').strip()
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_telegram_message(chat_id, text, reply_markup=None):
    """Универсальная функция отправки сообщений"""
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        return None

# --- МАРШРУТЫ (Routes) ---

@app.route('/', methods=['GET', 'POST'])
def root():
    return handle_request()

@app.route('/api/index', methods=['GET', 'POST'])
def api_index():
    return handle_request()

@app.route('/test', methods=['GET', 'POST'])
def test():
    return handle_request()

def handle_request():
    # 1. Обработка GET-запросов (проверка связи через браузер)
    if request.method == 'GET':
        return "✅ СЕРВЕР РАБОТАЕТ СТАБИЛЬНО! Теперь просто напиши /start в Telegram.", 200
    
    # 2. Проверка наличия токена
    if not TOKEN:
        logger.error("КРИТИЧЕСКАЯ ОШИБКА: BOTTOKEN не найден в Environment Variables!")
        return "Error: BOTTOKEN missing", 500

    # 3. Обработка POST-запросов (сообщения от Telegram)
    try:
        # Читаем данные как сырой текст и конвертируем в JSON вручную
        # Это исключает ошибки 400 и 415
        raw_data = request.data.decode('utf-8')
        if not raw_data:
            return "OK", 200
            
        data = json.loads(raw_data)
        logger.info("--- ПОЛУЧЕНО СООБЩЕНИЕ ОТ TELEGRAM ---")

        if 'message' not in data:
            return "OK", 200

        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '').strip()

        # --- ЛОГИКА БОТА ---
        if text == '/start':
            markup = {
                "keyboard": [
                    ["🏙 Купить квартиру", "🏠 Купить дом"],
                    ["📞 Контакты"]
                ],
                "resize_keyboard": True
            }
            send_telegram_message(chat_id, "Добро пожаловать в бот по недвижимости в Польше! 🇵🇱", json.dumps(markup))
        
        elif text == '🏙 Купить квартиру':
            send_telegram_message(chat_id, "🔎 Загружаю актуальные предложения по квартирам...")
        
        elif text == '🏠 Купить дом':
            send_telegram_message(chat_id, "🔎 Загружаю лучшие предложения по домам...")
        
        elif text == '📞 Контакты':
            send_telegram_message(chat_id, "📲 Свяжитесь с нами для консультации: +48 XXX XXX XXX")
        
        else:
            send_telegram_message(chat_id, f"Я пока не знаю команду '{text}', но скоро научусь!")

        return "OK", 200

    except Exception as e:
        logger.error(f"Ошибка обработки запроса: {e}")
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    # Запуск локально (для тестов)
    app.run(host='0.0.0.0', port=5000)
