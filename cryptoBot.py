from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from decouple import config
import cryptoBot_func

bot = Bot(config('TELEGRAM_API_URI'))

updater = Updater(config('TELEGRAM_API_URI'))

updater.dispatcher.add_handler(CommandHandler('hello', cryptoBot_func.hello))
updater.dispatcher.add_handler(CommandHandler('Owned', cryptoBot_func.owned_crypto))

updater.start_polling()
updater.idle()