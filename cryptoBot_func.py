from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from db import db

def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')

# def test():
#     test= {
#         "test1":"Test"
#     }
#     crypto = db.owned_crypto
#     crypto_id = crypto.insert_one(test)
#     print('Added')

def bought_crypto():
    pass


def owned_crypto(update: Update, context: CallbackContext):
    crypto = db.owned_crypto
    data = crypto.find()
    arr = []
    for d in data:
        arr.append(f'Crypto: {d["name"]}, Tokens: {d["tokens"]}, PurchasedAt: {d["boughtAt"]}\n -----\n')
    update.message.reply_text("".join(arr))

#?SET INTERVAL ALERTS