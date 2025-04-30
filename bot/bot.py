from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os
from datetime import datetime

TOKEN = '7947294849:AAF62sa6FmIJkRQ93s_oP5t1nYJipT6rkco'


class SurveyBot:
    def __init__(self):
        self.current_question = {}
        self.answers = {}

        os.makedirs('telegram_logs', exist_ok=True)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        self.current_question[chat_id] = 1
        self.answers[chat_id] = []

        await update.message.reply_text('Начинаем опрос!')
        self.ask_question(chat_id, 1)

    def ask_question(self, chat_id, question_number):
        questions = {
            1: ('Бот работает?', ['Истина', 'Ложь']),
            2: ('Здесь будет вопрос', ['Окей', 'Понятно', 'Потом подредактирую']),
            3: ('Привет, мир', ['Привет', 'Здарова', 'Пока'])
        }

        if question_number <= len(questions):
            question, options = questions[question_number]
            keyboard = [[option] for option in options]

            reply_markup = {'keyboard': keyboard}
            Update.message.reply_text(question, reply_markup=reply_markup)
        else:
            self.finish_survey(chat_id)

    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if chat_id in self.current_question:
            question_num = self.current_question[chat_id]
            answer = update.message.text

            folder_path = f'telegram_logs/vopros_{question_num}'
            os.makedirs(folder_path, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            with open(os.path.join(folder_path, f'{timestamp}.txt'), 'w') as f:
                f.write(answer)

            self.answers[chat_id].append(answer)

            if question_num < 3:
                self.current_question[chat_id] += 1
                self.ask_question(chat_id, self.current_question[chat_id])
            else:
                self.finish_survey(chat_id)

    def finish_survey(self, chat_id):
        Update.message.reply_text('Спасибо за участие в опросе!')
        del self.current_question[chat_id]
        del self.answers[chat_id]

def main():
    bot = SurveyBot()

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', bot.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_answer))

    application.run_polling()

if __name__ == '__main__':
    main()