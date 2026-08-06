import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Ваша ссылка на Google Таблицу (Apps Script)
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbwyB8eXzV6zOeufpaGJE1dJmY1wTxaNEHhFJKMpTFwPaUprJOISk2UagyhGhJdPjQLriQ/exec"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"].get("text", "")
        username = data["message"]["from"].get("username", "Anonymous")
        
        ai_response = "Здравствуйте! Чем могу помочь по недвижимости в Польше?"
        
        save_lead_to_sheet(username, user_message, ai_response)
        
    return {"status": "ok"}

def save_lead_to_sheet(username, message, ai_response):
    from datetime import datetime
    payload = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "message": message,
        "ai_response": ai_response
    }
    try:
        requests.post(GOOGLE_SHEET_URL, json=payload)
    except Exception as e:
        print("Ошибка записи в таблицу:", e)

if name == '__main__':
    app.run(debug=True)