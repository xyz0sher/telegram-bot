import telebot
from flask import Flask, request
import os

API_TOKEN = os.environ.get("8141830781:AAFNN8MDt0DTemaXiFKPgVNOrF7VRrpv5uk")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ================= BOT DATA =================

user_data = {}

CLASSES = ['10', '11', '12']
SUBJECTS = {
    '10': ['Maths', 'Science'],
    '11': ['Physics', 'Chemistry', 'Maths', 'Biology', 'Accountancy', 'Business', 'Economics', 'English', 'Computer'],
    '12': ['Physics', 'Chemistry', 'Maths', 'Biology', 'Accountancy', 'Business', 'Economics', 'English', 'Computer Science']
}
YEARS = ['2025', '2024', '2023', '2022', '2021']

# ================= BOT LOGIC =================

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for cls in CLASSES:
        markup.add(cls)
    bot.send_message(message.chat.id, "📚 Welcome! Select your class:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in CLASSES)
def choose_subject(message):
    user_data[message.chat.id]['class'] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for sub in SUBJECTS[message.text]:
        markup.add(sub)
    bot.send_message(message.chat.id, "📘 Choose subject:", reply_markup=markup)

@bot.message_handler(func=lambda m: any(m.text in SUBJECTS[c] for c in SUBJECTS))
def choose_year(message):
    user_data[message.chat.id]['subject'] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for year in YEARS:
        markup.add(year)
    bot.send_message(message.chat.id, "📅 Choose year:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in YEARS)
def send_paper(message):
    chat_id = message.chat.id
    cls = user_data[chat_id]['class']
    subject = user_data[chat_id]['subject']
    year = message.text

    path = f"papers/class{cls}/{subject.lower().replace(' ', '')}/{year}.pdf"

    if os.path.exists(path):
        with open(path, 'rb') as f:
            bot.send_document(chat_id, f)
    else:
        bot.send_message(chat_id, "❌ Paper not available.")

# ================= WEBHOOK =================

@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(
        request.stream.read().decode("utf-8")
    )
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "Bot is running!"

# ================= RUN =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
