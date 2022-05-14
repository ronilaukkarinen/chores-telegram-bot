#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Telegram Chores bot.
"""

import logging
import os
import json
import ynab_api
from ynab_api.rest import ApiException
from pprint import pprint
from telegram import ForceReply, Update
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

# YNAB related settings
configuration = ynab_api.Configuration()
# Configure API key authorization: bearer
budget_id = os.getenv('YNAB_BUDGET_ID')
category_id = os.getenv('YNAB_CATEGORY_ID')
configuration.api_key['Authorization'] = os.getenv('YNAB_PERSONAL_ACCESS_TOKEN')
configuration.api_key_prefix['Authorization'] = 'Bearer'

# Defining host is optional and default to https://api.youneedabudget.com/v1
configuration.host = "https://api.youneedabudget.com/v1"

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

# Get balance
def balance(update: Update, context: CallbackContext):
    """
    the callback for handling start command
    """
    bot: Bot = context.bot

    categories = ynab_api.CategoriesApi(ynab_api.ApiClient(configuration))

    try:
        api_response = categories.get_category_by_id(budget_id, category_id)
        balance = str(round(api_response.data.category.balance / 1000, 2))

        bot.send_message(
            chat_id=update.effective_chat.id,
            text=
            "Säästöön on kertynyt on tällä hetkellä yhteensä <b>{} €</b>".format(balance),
            parse_mode=ParseMode.HTML,
        )

    except ApiException as e:
        print("Tapahtui rajapintavirhe, @rollee: %s\n" % e)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Päivitys "%s" aiheutti virheen "%s"', update, context.error)

def start(update: Update, context: CallbackContext):
    """
    Show choices.
    """

    # defining the keyboard layout
    kbd_layout = [
      ['💰 Katso saldo'],
      ['Olohuoneen siivoaminen tavaroista (🪙 0.50 €)'],
      ['Lastenhuoneen siivoaminen (🪙 1.00 €)'],
      ['Tiskikoneen täyttö (🪙 0.50 €)',],
      ['Tiskikoneen tyhjennys ja tiskipöydän siivous (esim. pullot kassiin) (🪙 1.00 €)'],
      ['Kaikki kodin vaatteet narulle (🪙 1.00 €)'],
      ['Kaikki kodin vaatteet ja pyyhkeet kaappeihin 3 €'],
      ['Ruoat jääkaappiin kassista (🪙 0.50 €)'],
      ['Roskien vienti (🪙 1.00 €)'],
      ['Läksyt (tehtävä, jotta saa karkkirahan)'],
      ['Kokeesta 9 tai enemmän (💶 5 €)'],
    ]

    # converting layout to markup
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.replykeyboardmarkup.html
    kbd = ReplyKeyboardMarkup(kbd_layout)

    # sending the reply so as to activate the keyboard
    update.message.reply_text(text="Valitse oheisistä kotitöistä. Huom, lisää vain jos on tehty! Kerro myös milloin teit, jos lisäät myöhemmin.", reply_markup=kbd)

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


def dosomething(update: Update, context: CallbackContext):
    """
    the callback for handling start command
    """
    bot: Bot = context.bot

    if 'Olohuoneen' in update.message.text:
      bot.send_message(
          chat_id=update.effective_chat.id,
          text=
          "Hienoa! 👏 Kiitos olohuoneen siivoamisesta! 🥰\n<b>🪙 0.50 € on lisätty YNABiin Lotan säästöihin!</b>",
          parse_mode=ParseMode.HTML,
      )

    if 'saldo' in update.message.text:
      balance(update, context)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.getenv('TOKEN'), use_context=True)

    # Commands
    updater.dispatcher.add_handler(CommandHandler("ohje", help))
    updater.dispatcher.add_handler(CommandHandler("kotihommat", start))
    updater.dispatcher.add_handler(CommandHandler("peru", remove))
    updater.dispatcher.add_handler(CommandHandler("saldo", balance))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, dosomething))

    # Debug & init:
    # Log all errors
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
