#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Telegram Chores bot.
"""

import logging
import os
from telegram.forcereply import ForceReply
from telegram.ext.filters import Filters
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.parsemode import ParseMode

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Help
def help(update: Update, context: CallbackContext):
    """
    the callback for handling start command
    """
    bot: Bot = context.bot

    # Added HTML Parser to the existing command handler
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.parsemode.html#telegram.ParseMode.HTML
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "Tervetuloa käyttämään <b>Rollen Rahabottia</b>. Botin käyttäminen on hyvin yksinkertaista. Voit painaa /-nappia hymiöiden/tarrojen vieressä oikeassa alalaidassa tai kirjoittaa / nähdäksesi kaikki komennot. Kysy apua @rollee:lta jos menee sormi suuhun.",
        parse_mode=ParseMode.HTML,
    )

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Päivitys "%s" aiheutti virheen "%s"', update, context.error)

def start(update: Update, context: CallbackContext):
    """
    Show choices.
    """

    # defining the keyboard layout
    kbd_layout = [['Option 1', 'Option 2'], ['Option 3', 'Option 4'],
                       ["Option 5"]]

    # converting layout to markup
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.replykeyboardmarkup.html
    kbd = ReplyKeyboardMarkup(kbd_layout)

    # sending the reply so as to activate the keyboard
    update.message.reply_text(text="Select Options", reply_markup=kbd)

def remove(update: Update, context: CallbackContext):
    """
    Hide choices.
    """

    # making a reply markup to remove keyboard
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.replykeyboardremove.html
    reply_markup = ReplyKeyboardRemove()

    # sending the reply so as to remove the keyboard
    update.message.reply_text(text="Valinnat piilotettu.", reply_markup=reply_markup)
    pass


def echo(update: Update, context: CallbackContext):
    """
    message to handle any "Option [0-9]" Regrex.
    """
    # sending the reply message with the selected option
    update.message.reply_text("You just clicked on '%s'" % update.message.text)
    pass

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.getenv('TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("ohje", help))
    updater.dispatcher.add_handler(CommandHandler("kotihomma", start))
    updater.dispatcher.add_handler(CommandHandler("peru", remove))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r"Option [0-9]"), echo))

    # Debug & init:
    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
