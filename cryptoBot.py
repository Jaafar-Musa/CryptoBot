from telegram import Bot, Update, Message,ReplyKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters,MessageHandler,ConversationHandler
from decouple import config
import cryptoBot_func
import math
import random

#Keyboard
#  
SELECTED_OPTION, SELECT_CRYPTO,SELECT_PRICE, TYPED_OPTION = range(4)
# SELECTED_CHOICE, REPLY, TYPED_CHOICE =range(3)
keyboard_options = [
    ['Owned', 'Portfolio'],
    ['Profit from', 'Total profit'],
    ['Bought', 'Sold'],
    ['Other', 'Done']
]
# one_time_keyboard=True
markup = ReplyKeyboardMarkup(keyboard_options, )
def start(update:Update, context:CallbackContext): 
    update.message.reply_text('Hello Jaaf, How can I help you today?', reply_markup=markup)
    return SELECTED_OPTION


# def done(update: Update, context: CallbackContext) -> int:
#     user_data = context.user_data
#     if 'choice' in user_data:
#         del user_data['choice']

#     update.message.reply_text(
#         f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
#         reply_markup=ReplyKeyboardRemove(),
#     )

#     user_data.clear()
#     return ConversationHandler.END

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
                MessageHandler(Filters.regex('^Profit from$'), cryptoBot_func.profit_from),
                MessageHandler(Filters.regex('^Total profit$'), cryptoBot_func.total_profit),
                MessageHandler(Filters.regex('^Bought$'), cryptoBot_func.bought_crypto),
            ],
            SELECT_CRYPTO: [
                MessageHandler( Filters.text & (~Filters.command), cryptoBot_func.select_crypto)
            ],
            SELECT_PRICE:[
                MessageHandler( Filters.text & (~Filters.command), cryptoBot_func.select_price)                
            ]
            },
        fallbacks=[]
    )

    # dispatcher.add_handler(CommandHandler('start',cryptoBot_func.start, Filters.user(username="@JaafarMusa")))
    # dispatcher.add_handler(CommandHandler('help',cryptoBot_func.help, Filters.user(username="@JaafarMusa")))
    dispatcher.add_handler(conversation_handler)




    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
