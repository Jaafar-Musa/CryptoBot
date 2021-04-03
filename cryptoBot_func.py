from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
from db import db
from marketAPI import get_current_price

# SELECTED_CHOICE, REPLY, TYPED_CHOICE =range(3)
SELECTED_OPTION, SELECT_CRYPTO,SELECT_PRICE, TYPED_OPTION = range(4)
keyboard_options = [
    ['Owned', 'Portfolio'],
    ['Profit from', 'Total profit'],
    ['Bought', 'Sold'],
    ['Other', 'Done']
]
markup = ReplyKeyboardMarkup(keyboard_options)


def help(update:Update, context:CallbackContext): 
    update.message.reply_text('''
    Here is a list of things I can do:
    -- Show OWNED crypto /owned , -- Show PORTFOLIO ,
    -- Show Profit From /profitfrom, -- Show Total Profit /totalprofit ,
    -- Sold tokens, -- Bought tokens,
    ''')


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
    return SELECTED_OPTION


def select_crypto(update: Update, context: CallbackContext):
    print('this is selected: ', context.user_data)
    user_data = context.user_data
    user_data["token"] = update.message.text.upper()
    if context.user_data["choice"] in "Profit from":
        return profit_from(update, context)
    elif context.user_data["choice"] in ["Bought","Sold"]:
        print('hi')
        return SELECT_PRICE


def select_price(update: Update, context: CallbackContext):
    print('select price')
    user_data = context.user_data
    user_data["price"] = int(update.message.text)
    if context.user_data["choice"] in "Bought":
        return bought_crypto(update, context)
    elif context.user_data["choice"] in "Sold":
        return sold_crypto(update, context)


def bought_crypto(update: Update, context:CallbackContext):
    if update.message.text == "Bought":
        user_data = context.user_data
        user_data["choice"] = "Bought"
        update.message.reply_text("Which crypto did you buy?")
        return SELECT_CRYPTO
    token = context.user_data["token"]
    price = context.user_data["price"]
    update.message.reply_text(f'You bought {token} at {price}', reply_markup=markup)
    return SELECTED_OPTION


def sold_crypto():
    # user gives the token, and the price its sold at
    # bot calc the profit. if + then DCA the bought at price for said crypto
    # returns profit from sale

    pass


def profit_from(update: Update, context:CallbackContext):
    # ? RESET STATE AFTERWARDS
    if update.message.text == 'Profit from':
        update.message.reply_text("Which crypto do you want the profit of calculated?")
        user_data = context.user_data
        user_data["choice"] = update.message.text
        print(user_data)
        return SELECT_CRYPTO
    else:
        token = context.user_data["token"]
        update.message.reply_text(f'you chose {token}',reply_markup=markup)
        return SELECTED_OPTION
    

def total_profit(update:Update, context:CallbackContext):
    update.message.reply_text("Your total profit is..")
    # returns total profit
    #? +20 x%
    # crypto = db.owned_crypto
    # data = crypto.find()
    # get_current_price("BTC")
    # # for d in data:


def portfolio(update: Update, context:CallbackContext):
    update.message.reply_text("This is your portfolio")
    return SELECTED_OPTION

