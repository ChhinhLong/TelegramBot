from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# PDF data for two sections
exam_files = ['pdf/exam_1.pdf', 'pdf/exam_2.pdf', 'pdf/exam_3.pdf']
solution_files = ['pdf/solution_1.pdf', 'pdf/solution_2.pdf', 'pdf/solution_3.pdf']

# Keep track of user states
user_state = {}

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    reply_markup = ReplyKeyboardMarkup([['វិញ្ញាសា', 'កំណែ']], resize_keyboard=True)
    update.message.reply_text(f"សូមស្វាគមន៍ {user.first_name} ចុចប៊ូតុងខាងក្រោម", reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    if text == "វិញ្ញាសា":
        user_state[chat_id] = {"section": "exam", "index": 0}
        send_pdf(update, context, chat_id)

    elif text == "កំណែ":
        user_state[chat_id] = {"section": "solution", "index": 0}
        send_pdf(update, context, chat_id)

    elif text == "Next":
        if chat_id not in user_state:
            update.message.reply_text("សូមជ្រើសរើស វិញ្ញាសា ឬ កំណែ ជាមុនសិន")
            return
        state = user_state[chat_id]
        state["index"] += 1
        send_pdf(update, context, chat_id)

    elif text == "Back":
        if chat_id not in user_state:
            update.message.reply_text("សូមជ្រើសរើស វិញ្ញាសា ឬ កំណែ ជាមុនសិន")
            return
        state = user_state[chat_id]
        if state["index"] > 0:
            state["index"] -= 1
        send_pdf(update, context, chat_id)

def send_pdf(update: Update, context: CallbackContext, chat_id):
    state = user_state[chat_id]
    section = state["section"]
    index = state["index"]

    files = exam_files if section == "exam" else solution_files
    reply_markup = ReplyKeyboardMarkup([['Back', 'Next']], resize_keyboard=True)

    if index < len(files):
        with open(files[index], 'rb') as f:
            context.bot.send_document(chat_id=chat_id, document=f, reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=chat_id, text="អស់🚫", reply_markup=reply_markup)
        state["index"] = len(files) - 1

def main():
    updater = Updater("8061129012:AAHfjZsON_1Ck8Sky2LLkJCU_R6CeYvN1Zw", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
