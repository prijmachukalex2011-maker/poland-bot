from flask import Flask, request
import telebot

# Ваш токен
TOKEN = '6891167516:AAeDb2H_S-S_1defu1_pnt_PqL068Dpw'
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# --- ОБРАБОТЧИКИ БОТА ---
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот работает на Vercel!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Вы написали: {message.text}")

# --- МАРШРУТ ДЛЯ VERCEL ---
@app.route('/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Получаем данные от Telegram
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        # Передаем обновление в бота
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Wrong method', 405

@app.route('/test')
def test():
    return "Bot is running!", 200

# Это нужно только для локального запуска, Vercel это игнорирует
if __name__ == "__main__":
    app.run()


