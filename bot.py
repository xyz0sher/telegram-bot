import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

API_TOKEN = '8141830781:AAEASzNIy-BT09SBcVwOLS5TNWdbUXy05g8'
bot = telebot.TeleBot(API_TOKEN)


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
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for cls in CLASSES:
        markup.add(KeyboardButton(cls))
    bot.send_message(message.chat.id, "📚 Welcome! Select your class:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in CLASSES)
def choose_subject(message):
    user_data[message.chat.id]['class'] = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in SUBJECTS[message.text]:
        markup.add(KeyboardButton(subject))
    bot.send_message(message.chat.id, f"📘 You selected Class {message.text}. Now choose a subject:", reply_markup=markup)

@bot.message_handler(func=lambda message: any(message.text in SUBJECTS[cls] for cls in CLASSES))
def choose_year(message):
    user_data[message.chat.id]['subject'] = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for year in YEARS:
        markup.add(KeyboardButton(year))
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

bot.polling()
