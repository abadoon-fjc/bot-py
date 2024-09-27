import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для получения курса валют
def get_exchange_rate(currency):
    response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{currency}')
    data = response.json()
    return data['rates']['RUB']

# Функция обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Euro", callback_data='euro'),
         InlineKeyboardButton("Dollar", callback_data='dollar')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добрый день. Как вас зовут?', reply_markup=reply_markup)

# Функция обработки нажатий на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    currency = 'EUR' if query.data == 'euro' else 'USD'
    exchange_rate = get_exchange_rate(currency)
    await query.edit_message_text(text=f'Курс {currency} сегодня: {exchange_rate} р.')

# Функция обработки текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.message.text
    keyboard = [
        [InlineKeyboardButton("Euro", callback_data='euro'),
         InlineKeyboardButton("Dollar", callback_data='dollar')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'Оооооо, {user_name}, вы вернулись! Что вы хотите узнать?', reply_markup=reply_markup)

def main() -> None:
    # Создаем приложение
    application = ApplicationBuilder().token('7665845880:AAHUFh2zGRcrsETD53Vd2HL5OCOw9da8TW8').build()

    # Обработчики команд и сообщений
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
