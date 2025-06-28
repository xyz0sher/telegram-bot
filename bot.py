import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Define classes, subjects and years
CLASSES = ['Class 9', 'Class 10', 'Class 11', 'Class 12']
SUBJECTS = {
    'Class 9': ['Maths', 'Science'],
    'Class 10': ['Maths', 'Science'],
    'Class 11': ['Physics', 'Chemistry'],
    'Class 12': ['Physics', 'Chemistry']
}
YEARS = ['2025', '2024', '2023', '2022', '2021']

# Store user choices
user_data = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {}  # reset progress
    reply = ReplyKeyboardMarkup([[c] for c in CLASSES], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("📚 Welcome! Please choose your class:", reply_markup=reply)

# Handle all messages (step-by-step selection)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_data:
        user_data[user_id] = {}

    data = user_data[user_id]
    print(f"User data so far: {data}")  # Debug

    # Step 1: Choose class
    if 'class' not in data:
        if text in CLASSES:
            data['class'] = text
            subjects = SUBJECTS[text]
            reply = ReplyKeyboardMarkup([[s] for s in subjects], one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text("✅ Great! Now select a subject:", reply_markup=reply)
        else:
            await update.message.reply_text("❌ Please select a valid class.")

    # Step 2: Choose subject
    elif 'subject' not in data:
        if text in SUBJECTS[data['class']]:
            data['subject'] = text
            reply = ReplyKeyboardMarkup([[y] for y in YEARS], one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text("📅 Choose the year of the paper:", reply_markup=reply)
        else:
            await update.message.reply_text("❌ Please choose a valid subject.")

    # Step 3: Choose year
    elif 'year' not in data:
        if text in YEARS:
            data['year'] = text
            await send_question_paper(update, context, data)
            user_data[user_id] = {}  # Reset after sending
        else:
            await update.message.reply_text("❌ Please choose a valid year.")

# Send PDF file if exists
async def send_question_paper(update: Update, context: ContextTypes.DEFAULT_TYPE, data):
    class_folder = data['class'].lower().replace(" ", "")
    subject_folder = data['subject'].lower()
    year_file = f"{data['year']}.pdf"
    path = f"papers/{class_folder}/{subject_folder}/{year_file}"

    if os.path.exists(path):
        await update.message.reply_document(document=open(path, 'rb'))
    else:
        await update.message.reply_text("⚠️ Sorry, that paper is not available.")

# Main function
def main():
    print("✅ Bot is starting...")
    app = Application.builder().token("7893556939:AAGV3RKJeS7Llzrkma6rYBW_Ubb-Dk-jaYo").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
