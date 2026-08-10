from flask import Flask, request
import telebot

# Токен вставляем прямо сюда
TOKEN = "8891147516:AAE5pZOd0nYZNr-bkNur1_pxKPQLO6BDWpw"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# --- ОБРАБОТЧИКИ ТЕЛЕГРАМ ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот для недвижимости в Польше успешно запущен и работает на Vercel!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Получено ваше сообщение: {message.text}")

# --- МАРШРУТЫ FLASK ---

@app.route('/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
        except Exception as e:
            print(f"Error processing update: {e}")
    return "OK", 200

@app.route('/test')
def index():
    return "Bot is running! Your server is alive!"

# Для Vercel эта часть не обязательна, но оставим для порядка
if __name__ == '__main__':
    app.run()
