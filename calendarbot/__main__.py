import hashlib
import logging
import os
import random
import sys

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
PORT = os.environ.get("PORT")
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
    # updater.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


############################ Keyboards #########################################
def main_menu_keyboard():
    keyboard = [[KeyboardButton('Aggiungi evento')],
                [KeyboardButton('Visualizza eventi')]]
    return keyboard


def add_event_menu_keyboard():
    keyboard = [[KeyboardButton('Gennaio')],
                [KeyboardButton('Febbraio')],
                [KeyboardButton('<<Indietro')]]
    return keyboard


def view_events_menu_keyboard():
    keyboard = [[KeyboardButton('Oggi')],
                [KeyboardButton('Questa settimana')],
                [KeyboardButton('Questo mese')],
                [KeyboardButton('<<Indietro')]]
    return keyboard


############################# Messages #########################################
def main_menu_message():
    return 'Seleziona un\'opzione nel menu principale:'


def add_event_menu_message():
    return 'In che mese vuoi aggiungere l\'evento?'


def view_events_menu_message():
    return 'Quali eventi vuoi visualizzare?'


################################ Handlers ######################################
def start_handler(update: Update, context: CallbackContext):
    # Creating a handler-function for /start command
    logger.info("User {} started bot".format(update.effective_user.id))
    update.message.reply_text(
        "Ciao, {}!\nPremi /menu per visualizzare le opzioni".format(update.effective_user.name))


def main_menu(update: Update, context):
    logger.info("User {} started bot".format(update.effective_user.id))
    context.bot.send_message(chat_id=update.effective_chat.id, text=main_menu_message(),
                             reply_markup=ReplyKeyboardMarkup(main_menu_keyboard()))


def add_event_menu(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=add_event_menu_message(),
                             reply_markup=ReplyKeyboardMarkup(add_event_menu_keyboard()))


def view_events_menu(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=view_events_menu_message(),
                             reply_markup=ReplyKeyboardMarkup(view_events_menu_keyboard()))


def message_handler(update: Update, context: CallbackContext):
    # Creating a handler-function for all messages
    logger.info("User {} sent message: {}".format(update.effective_user.id, update.message.text))
    if update.message.text == "Aggiungi evento":
        add_event_menu(update, context)  # todo: gestire la selezione del mese effettuata dall'utente
    if update.message.text == "Visualizza eventi":
        view_events_menu(update, context)  # todo: gestire la visualizzazione degli eventi


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start_handler))
    updater.dispatcher.add_handler(CommandHandler('menu', main_menu))
    updater.dispatcher.add_handler(CommandHandler('add_event', add_event_menu))
    updater.dispatcher.add_handler(CommandHandler('view_events', view_events_menu))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

    if "HEROKU" in list(os.environ.keys()):
        run_prod(updater)
    else:
        run_local(updater)
