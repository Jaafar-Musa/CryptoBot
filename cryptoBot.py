from telegram import Bot, Update, Message
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters,MessageHandler
from decouple import config
import cryptoBot_func
import math
import random

updater = Updater(config('TELEGRAM_API_URI'))
dispatcher = updater.dispatcher


def response(update:Update, context:CallbackContext):
    if update.message.text.lower() in ['hi','hello','sup']:
        greetings = ['Hello Jaaf', 'Common estas', 'Howdy', 'Hi Jaafs']
        rand = random.randint(0,len(greetings)-1)
        update.message.reply_text(greetings[rand])
    if update.message.text.lower() in ["owned"]:
        print('owned')
        

def help(update:Update, context:CallbackContext): 
    update.message.reply_text('''
    Here is a list of things I can do:
    -- Show OWNED crypto /owned , -- Show PORTFOLIO ,
    -- Show Profit From /profitfrom, -- Show Total Profit /totalprofit ,
    -- Sold tokens, -- Bought tokens,
    ''')


def start(update:Update, context:CallbackContext): 
    update.message.reply_text('Hello Jaaf, How can I help you today?')



def main():
    print('Bot started')
    updater = Updater(config('TELEGRAM_API_URI'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start',start, Filters.user(username="@JaafarMusa")))
    dispatcher.add_handler(CommandHandler('help',help, Filters.user(username="@JaafarMusa")))
    dispatcher.add_handler(CommandHandler('owned',cryptoBot_func.owned_crypto, Filters.user(username="@JaafarMusa")))
    dispatcher.add_handler(CommandHandler('profitfrom',cryptoBot_func.profit_from, Filters.user(username="@JaafarMusa")))
    dispatcher.add_handler(MessageHandler(Filters.text,response))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
