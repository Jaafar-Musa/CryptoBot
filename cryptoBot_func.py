from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from db import db

def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def bought_crypto():
    # user gives the token, and the price its bought at
    #  calculates and returns dca
    pass


def sold_crypto():
    # user gives the token, and the price its sold at
    # bot calc the profit. if + then DCA the bought at price for said crypto
    # returns profit from sale

    pass


def profit_from():
    # returns profits from individual tokens
    #? $ADA +$20 up by x%
    pass


def total_profit():
    # returns total profit
    #? +20 x%
    pass


def portfolio():
    # returns percentages of crypto holdings
    #? $ADA 60% $LINK 40%
    pass


def owned_crypto(update: Update, context: CallbackContext):
    # Returns all owned crypto
    msg = update.message.text
    print(msg)
    crypto = db.owned_crypto
    data = crypto.find()
    arr = []
    for d in data:
        arr.append(f'Crypto: {d["name"]}, Tokens: {d["tokens"]}, PurchasedAt: {d["boughtAt"]}\n -----\n')
    update.message.reply_text("".join(arr))

#?SET INTERVAL ALERTS