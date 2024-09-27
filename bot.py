import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_exchange_rate():
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    data = response.json()
    return data['rates']['RUB']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Добрый день. Как вас зовут?')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.message.text
    exchange_rate = get_exchange_rate()
    await update.message.reply_text(f'Рад знакомству, {user_name}! Курс доллара сегодня {exchange_rate} р.')

def main() -> None:
    application = ApplicationBuilder().token('7665845880:AAHUFh2zGRcrsETD53Vd2HL5OCOw9da8TW8').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
