from telegram import Bot, Update, Message,ReplyKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters,MessageHandler,ConversationHandler
from decouple import config
import cryptoBot_func
import math
import random

SELECTED_OPTION, SELECT_CRYPTO,SELECT_PRICE, CONFIRMATION, ACTION, INDIVIDUAL = range(6)

def start(update:Update, context:CallbackContext): 
    update.message.reply_text('Hello Jaaf, How can I help you today?', reply_markup=cryptoBot_func.markup_default_options)
    return SELECTED_OPTION


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("I don't understand you")
    return SELECTED_OPTION
    


def main():
    print('Bot started')
    updater = Updater(config('TELEGRAM_API_URI'))
    dispatcher = updater.dispatcher
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, Filters.user(username='@JaafarMusa'))],
        states={
            SELECTED_OPTION: [
                MessageHandler(Filters.regex('^Owned$'), cryptoBot_func.owned_crypto),
                MessageHandler(Filters.regex('^Portfolio$'), cryptoBot_func.portfolio),
                MessageHandler(Filters.regex('^Actions$'), cryptoBot_func.return_Action),
                MessageHandler(Filters.regex('^Individual$'), cryptoBot_func.return_Individual),
                MessageHandler(Filters.regex('^Total profit$'), cryptoBot_func.total_profit),
                MessageHandler(Filters.regex('^Done$'), cryptoBot_func.done),
                # MessageHandler(Filters.regex('^Bought$'), cryptoBot_func.bought_crypto),
                # MessageHandler(Filters.regex('^Sold$'), cryptoBot_func.sold_crypto),
            ],
            SELECT_CRYPTO: [
                MessageHandler( Filters.text & (~Filters.command), cryptoBot_func.select_crypto)
            ],
            SELECT_PRICE:[
                MessageHandler( Filters.text & (~Filters.command), cryptoBot_func.select_price)                
            ],
            CONFIRMATION:[
                MessageHandler(Filters.regex('^(Yes|No)$'), cryptoBot_func.confirmation),                
            ],
            ACTION:[
                MessageHandler(Filters.regex('^Bought$'), cryptoBot_func.bought_crypto),                
                MessageHandler(Filters.regex('^Sold$'), cryptoBot_func.sold_crypto),
                MessageHandler(Filters.regex('^Back$'), cryptoBot_func.back),                  
            ],
            INDIVIDUAL:[
                MessageHandler(Filters.regex('^test$'), cryptoBot_func.confirmation),
                MessageHandler(Filters.regex('^Back$'), cryptoBot_func.back),                    
            ],
            },
        fallbacks=[CommandHandler('unknown', unknown)]
    )
    dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
