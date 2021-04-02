from telegram import Bot, Update, Message
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters,MessageHandler
from decouple import config
import cryptoBot_func

def response(update:Update, context:CallbackContext):
    if 'hi' in update.message.text:
        update.message.reply_text('hiiiii')
    

def help(update:Update, context:CallbackContext): 
    update.message.reply_text('helppppp')


def main():
    updater = Updater(config('TELEGRAM_API_URI'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('help',help))
    dispatcher.add_handler(MessageHandler(Filters.text,response))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
