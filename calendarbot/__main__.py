from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
import os


async def hello(update: Update, context) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('TG_TOKEN')).build()
    app.add_handler(CommandHandler("hello", hello))
    app.run_polling()


