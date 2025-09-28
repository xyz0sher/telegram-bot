import telebot
from flask import Flask, request
import os

API_TOKEN = '8141830781:AAHJ1WCFZ_xdP2fyAPwqzcZqX1L1yWSJAqo'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ==== Bot logic same as before ====

user_data = {}

CLASSES = ['10', '11', '12']
SUBJECTS = {
    '10': ['Maths', 'Science'],
    '11': ['Physics', 'Chemistry', 'Maths', 'Biology', 'Accountancy', 'Business', 'Economics', 'English', 'Computer'],
    '12': ['Physics', 'Chemistry', 'Maths', 'Biology', 'Accountancy', 'Business', 'Economics', 'English', 'Computer Science']
}
YEARS = ['2025', '2024', '2023', '2022', '2021']

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for cls in CLASSES:
        markup.add(telebot.types.KeyboardButton(cls))
    bot.send_message(message.chat.id, "📚 Welcome! Select your class:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in CLASSES)
def choose_subject(message):
    user_data[message.chat.id]['class'] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in SUBJECTS[message.text]:
        markup.add(telebot.types.KeyboardButton(subject))
    bot.send_message(message.chat.id, f"📘 You selected Class {message.text}. Now choose a subject:", reply_markup=markup)

@bot.message_handler(func=lambda message: any(message.text in SUBJECTS[cls] for cls in CLASSES))
def choose_year(message):
    user_data[message.chat.id]['subject'] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for year in YEARS:
        markup.add(telebot.types.KeyboardButton(year))
    bot.send_message(message.chat.id, f"📅 Select year of question paper:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in YEARS)
def send_paper(message):
    chat_id = message.chat.id
    year = message.text
    cls = user_data[chat_id].get('class')
    subject = user_data[chat_id].get('subject')

    file_path = f"papers/class{cls}/{subject.lower().replace(' ', '')}/{year}.pdf"

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            bot.send_document(chat_id, f, caption=f"📄 {subject} - {year} Question Paper")
    else:
        bot.send_message(chat_id, "❌ Paper not found. Please check if it's uploaded.")

# ==== Webhook code ====

@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/')
def home():
    return 'Bot is alive!'

# Set webhook when app starts
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://telegram-bot-rq96.onrender.com/8141830781:AAFAIyBQ38nFqGjDelRz_hHBfacJlh_Qojk")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
