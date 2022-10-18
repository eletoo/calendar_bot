import hashlib
import logging
import os
import random
import sys

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
PORT = int(os.environ.get("PORT"))
TOKEN = os.getenv("TG_TOKEN")


def run_local(updater: Updater):
    updater.start_polling()


def run_prod(updater):
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    path = hashlib.md5(TOKEN.encode("utf-8")).hexdigest()
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=path)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, path))


def start_handler(update: Update, context: CallbackContext):
    # Creating a handler-function for /start command
    logger.info("User {} started bot".format(update.effective_user.id))
    update.message.reply_text(f"Hello from Python, {update.effective_user.name}!\nPress /random to get random number")


def random_handler(update: Update, context: CallbackContext):
    # Creating a handler-function for /random command
    number = random.randint(0, 10)


def message_handler(update: Update, context: CallbackContext):
    # Creating a handler-function for all messages
    logger.info("User {} sent message: {}".format(update.effective_user.id, update.message.text))
    update.message.reply_text("You sent me: {}".format(update.message.text))


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("addevent", random_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

    if "HEROKU" in list(os.environ.keys()):
        run_prod(updater)
    else:
        run_local(updater)
