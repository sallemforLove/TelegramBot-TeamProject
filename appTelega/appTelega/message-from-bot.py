from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler
import json
from datetime import datetime
import os

TOKEN = '7003418980:AAH-qwhqVxDONvEAXKOoVbtseVeKlFQStM4'
BASE_DIR = 'telegram_logs'

QUESTIONS = [
    "Бот работает?",
    "Здесь будет вопрос",
    "Привет, мир"
]

BUTTONS = [
    ["Истина", "Ложь"],
    ["Окей", "Понятно", "Потом подредактирую"],
    ["Привет", "Здарова", "Пока"]
]


async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Давайте начнем опрос!"
    )
    context.user_data['current_question'] = 0
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=QUESTIONS[0],
        reply_markup={'keyboard': [[button] for button in BUTTONS[0]], 'resize_keyboard': True,
                      'one_time_keyboard': True}
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Пройти опрос':
        await start_survey(update, context)
        return

    if 'current_question' not in context.user_data:
        await update.message.reply_text('Напишите "Пройти опрос", чтобы начать')
        return

    current_question = context.user_data['current_question']
    if current_question >= len(QUESTIONS):
        await update.message.reply_text('Опрос завершен!')
        context.user_data.clear()
        return

    save_answer(update, context)

    next_question = current_question + 1
    if next_question < len(QUESTIONS):
        context.user_data['current_question'] = next_question
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=QUESTIONS[next_question],
            reply_markup={'keyboard': [[button] for button in BUTTONS[next_question]], 'resize_keyboard': True,
                          'one_time_keyboard': True}
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Спасибо за участие в опросе!",
            reply_markup={'keyboard': [], 'resize_keyboard': True}
        )
        context.user_data.clear()


def save_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_data = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'chat_id': update.message.chat.id,
        'user_id': update.message.from_user.id,
        'username': update.message.from_user.username,
        'question': QUESTIONS[context.user_data['current_question']],
        'answer': update.message.text
    }

    question_dir = f"{BASE_DIR}/вопрос_{context.user_data['current_question'] + 1}"
    os.makedirs(question_dir, exist_ok=True)
    filename = f"{question_dir}/message_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(message_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'Ошибка при сохранении ответа: {str(e)}')


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start_survey))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()