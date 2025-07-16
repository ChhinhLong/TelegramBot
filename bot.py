import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# បញ្ចូល Token ពី environment variable
BOT_TOKEN = os.getenv("8061129012:AAHfjZsON_1Ck8Sky2LLkJCU_R6CeYvN1Zw")

# ផ្លូវឯកសារ PDF
exam_files = ['pdf/exam_1.pdf', 'pdf/exam_2.pdf', 'pdf/exam_3.pdf']
solution_files = ['pdf/solution_1.pdf', 'pdf/solution_2.pdf', 'pdf/solution_3.pdf']

# ការរក្សាទុកស្ថានភាពអ្នកប្រើ
user_state = {}

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    keyboard = [['វិញ្ញាសា', 'កំណែ']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        f"សូមស្វាគមន៍ {user.first_name} ចុចប៊ូតុងខាងក្រោម",
        reply_markup=reply_markup
    )

def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text.strip()

    if text == "វិញ្ញាសា":
        user_state[chat_id] = {"section": "exam", "index": 0}
        send_pdf(update, context, chat_id)

    elif text == "កំណែ":
        user_state[chat_id] = {"section": "solution", "index": 0}
        send_pdf(update, context, chat_id)

    elif text == "Next":
        if chat_id in user_state:
            state = user_state[chat_id]
            state["index"] += 1
            send_pdf(update, context, chat_id)
        else:
            update.message.reply_text("សូមជ្រើសរើស វិញ្ញាសា ឬ កំណែ ជាមុនសិន។")

    elif text == "Back":
        if chat_id in user_state:
            state = user_state[chat_id]
            if state["index"] > 0:
                state["index"] -= 1
            send_pdf(update, context, chat_id)
        else:
            update.message.reply_text("សូមជ្រើសរើស វិញ្ញាសា ឬ កំណែ ជាមុនសិន។")

def send_pdf(update: Update, context: CallbackContext, chat_id):
    state = user_state[chat_id]
    section = state["section"]
    index = state["index"]

    files = exam_files if section == "exam" else solution_files
    keyboard = [['Back', 'Next']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if index < len(files):
        file_path = files[index]
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                context.bot.send_document(chat_id=chat_id, document=f, reply_markup=reply_markup)
        else:
            context.bot.send_message(chat_id=chat_id, text="ឯកសារមិនមានទេ។")
    else:
        context.bot.send_message(chat_id=chat_id, text="អស់🚫", reply_markup=reply_markup)
        state["index"] = len(files) - 1  # reset index

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
