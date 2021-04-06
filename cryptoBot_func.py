from telegram import Bot, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove 
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler
from db import db
from marketAPI import get_current_price

SELECTED_OPTION, SELECT_CRYPTO,SELECT_PRICE, CONFIRMATION, ACTION, INDIVIDUAL = range(6)
keyboard_default_options = [
    ['Owned', 'Portfolio'],
    ['Individual', 'Total profit'],
    ['Actions', 'Done'],
]
keyboard_confirmation_options = [
    ['Yes', 'No'],
]
keyboard_actions_options = [
    ['Bought', 'Sold'],
    ['Invested', 'Withdrew'],
    ['Back'],
]
keyboard_individual_options = [
    ['Token', 'Token'],
    ['Token', 'Back'],
]
markup_default_options = ReplyKeyboardMarkup(keyboard_default_options,one_time_keyboard=True)
markup_confirmation_options = ReplyKeyboardMarkup(keyboard_confirmation_options,one_time_keyboard=True)
markup_actions_options = ReplyKeyboardMarkup(keyboard_actions_options,one_time_keyboard=True)
markup_individual_options = ReplyKeyboardMarkup(keyboard_individual_options,one_time_keyboard=True)

def return_Action(update: Update, context: CallbackContext):
    update.message.reply_text("What action did you perform?", reply_markup=markup_actions_options)
    return ACTION


def return_Individual(update: Update, context: CallbackContext):
    update.message.reply_text("What info do you want to know about the token?", reply_markup=markup_individual_options)
    return INDIVIDUAL


def back(update: Update, context: CallbackContext):
    update.message.reply_text("Select an Option.", reply_markup=markup_default_options)
    return SELECTED_OPTION

def owned_crypto(update: Update, context: CallbackContext):
    try:
        crypto = db.owned_crypto
        data = crypto.find({})
        arr = []
        for d in data:
            arr.append(f'Crypto: {d["name"]}, Tokens: {d["tokens"]}, PurchasedAt: ${d["boughtAt"]}\n -----\n')
        update.message.reply_text("".join(arr),reply_markup=markup_default_options)
        return SELECTED_OPTION
    except Exception as e:
        print(e)
        update.message.reply_text("There was an error getting the data!")


def portfolio(update: Update, context:CallbackContext):
    try:
        crypto = db.owned_crypto
        data = crypto.find({})
        arr= []
        total = 0
        portfolio = []
        for d in data:
            m = d["tokens"] * d["boughtAt"]
            total += m
            arr.append([ d["name"],d["boughtAt"]])
        print(arr)
        for token in range(len(arr)):
            name = arr[token][0]
            amount = arr[token][1]
            percentage = round((amount/total) * 100,2)
            portfolio.append(f'{name}, accounts for {percentage}% of your portfolio\n')
        update.message.reply_text("".join(portfolio),reply_markup=markup_default_options)
        return SELECTED_OPTION
    except Exception as e:
        print(e)
        update.message.reply_text("There was an error!")


def total_profit(update:Update, context:CallbackContext):
    # WHEN FREE ADD PERCENTAGE INCREASE FROM INVESTMENT
    try:
        crypto = db.owned_crypto
        stats = db.stats
        invested = stats.find()
        amount_invested = 0
        for i in invested:
            amount_invested += i["amount_invested"]
        data = crypto.find({})
        total = 0
        for d in data:
            current_price = get_current_price(d["name"])
            print(current_price)
            total += (d["tokens"] * current_price)
        profit = total - amount_invested
        update.message.reply_text(f'Your current profit is: ${round(profit,2)}',reply_markup=markup_default_options)
        return SELECTED_OPTION
    except Exception as e:
        print(e)
        update.message.reply_text("There was an error!")


def profit_from(update: Update, context:CallbackContext):
    # replace btn with individual tokens
    update.message.reply_text(f'No function yet!',reply_markup=markup)
    # if update.message.text == 'Profit from':
    #     update.message.reply_text("Which crypto do you want the profit of calculated?")
    #     user_data = context.user_data
    #     user_data["choice"] = update.message.text
    #     print(user_data)
    #     return SELECT_CRYPTO
    # else:
    #     token = context.user_data["token"]
    #     update.message.reply_text(f'you chose {token}',reply_markup=markup)
    #     return SELECTED_OPTION
    
def confirmation(update: Update, context: CallbackContext):
    try:
        if update.message.text in "Yes":
            if context.user_data["choice"] in "Bought":
                return bought_crypto(update, context)
            if context.user_data["choice"] in "Sold":
                return sold_crypto(update, context)
        if update.message.text in "No":
            if context.user_data["choice"] in "Bought":
                update.message.reply_text("How many tokens did you buy?")
            if context.user_data["choice"] in "Sold":
                update.message.reply_text("How many tokens did you sell?")
            del context.user_data["token"]
            return SELECT_CRYPTO    
    except Exception as e:
        print(e)
        update.message.reply_text('There was an error.', reply_markup=markup_default_options)


def done(update: Update, context: CallbackContext):
    user_data = context.user_data
    update.message.reply_text(
        f"If you need me again, just /start me!",
        reply_markup=ReplyKeyboardRemove(),
    )
    user_data.clear()
    return ConversationHandler.END


def select_crypto(update: Update, context: CallbackContext):
    # add a cancel command!
    try:
        if context.user_data["priceSelected"] is False:
            if update.message.text.lower() in "back":
                del context.user_data["choice"]
                update.message.reply_text("Select a choice.", reply_markup=markup_default_options)
                return SELECTED_OPTION
            else:
                user_data = context.user_data
                user_data["name"] = update.message.text.upper()
                if context.user_data["choice"] in "Profit from":
                    return profit_from(update, context)
                if context.user_data["choice"] in "Bought":
                    update.message.reply_text("At what price did you buy the crypto?")
                    return SELECT_PRICE
                if context.user_data["choice"] in "Sold":
                    update.message.reply_text("At what price did you sell the crypto?")
                    return SELECT_PRICE
        else:
            if update.message.text.lower() in "back":
                context.user_data["priceSelected"] = False
                del context.user_data["price"]
                if context.user_data["choice"] in "Bought":
                    update.message.reply_text("At what price did you buy the crypto?")
                if context.user_data["choice"] in "Sold":
                    update.message.reply_text("At what price did you sell the crypto?")
                return SELECT_PRICE
            else:
                price = context.user_data["price"] 
                name = context.user_data["name"]
                user_data = context.user_data
                user_data["token"] = float(update.message.text)
                token = context.user_data["token"]
                update.message.reply_text(f"Are these the correct details?\n {token} {name} for ${price}", reply_markup=markup_confirmation_options)
                return CONFIRMATION
    except Exception as e:
        print(e)
        # ! clear states
        update.message.reply_text("There was an error")


def select_price(update: Update, context: CallbackContext):
    try:
        if update.message.text.lower() in "back":
            if context.user_data["choice"] in "Bought":
                update.message.reply_text("Which crypto did you buy?")
            if context.user_data["choice"] in "Sold":
                update.message.reply_text("Which crypto did you sell?")
            del context.user_data["name"]
            return SELECT_CRYPTO
        else:            
            user_data = context.user_data
            user_data["price"] = float(update.message.text)
            user_data["priceSelected"] = True
            if context.user_data["choice"] in "Bought":
                update.message.reply_text("At what price did you buy the crypto?")
            if context.user_data["choice"] in "Sold":
                update.message.reply_text("At what price did you sell the crypto?")
            return SELECT_CRYPTO
    except Exception as e:
        print(e)
        update.message.reply_text("There was an error")


def bought_crypto(update: Update, context:CallbackContext):
    try:
        if update.message.text == "Bought":
            user_data = context.user_data
            user_data["choice"] = "Bought"
            user_data["priceSelected"] = False
            update.message.reply_text("Which crypto did you buy?")
            return SELECT_CRYPTO
        token = context.user_data["token"]
        price = context.user_data["price"]
        name = context.user_data["name"]
        data = db.owned_crypto.find()
        dca = False
        old_token = 0.00
        old_price = 0.00
        for d in data:
            print(d)
            if d["name"] == name:
                old_price = d["boughtAt"]
                old_token = d["tokens"]
                dca = True
                break
        if dca:
            v1 = old_token * old_price
            v2 = context.user_data["price"] * context.user_data["token"]
            t_tokens = old_token + context.user_data["token"]
            dollar_cost_average = (v1 + v2)/t_tokens
            db.owned_crypto.update({'name':context.user_data["name"]}, {"$set":{'boughtAt': dollar_cost_average, 'tokens':t_tokens}})
            update.message.reply_text(f"You bought {name}, your new DCA is ${dollar_cost_average}", reply_markup=markup_default_options)
        else:
            db.owned_crypto.insert_one({"name":name, "boughtAt": context.user_data["price"], "tokens":context.user_data["token"]})
            update.message.reply_text(f'You bought {token} at {price}', reply_markup=markup_default_options)
        return SELECTED_OPTION
    except Exception as e:
        print(e)
        update.message.reply_text("There was an error here")


def sold_crypto(update: Update, context:CallbackContext):
    if update.message.text == "Sold":
        user_data = context.user_data
        user_data["choice"] = "Sold"
        user_data["priceSelected"] = False
        update.message.reply_text("Which crypto did you sell?")
        return SELECT_CRYPTO
    token = context.user_data["token"]
    price = context.user_data["price"]
    name = context.user_data["name"]
    data = db.owned_crypto.find()
    dca = False
    old_token = 0.00
    old_price = 0.00
    for d in data:
        print(d)
        if d["name"] == name:
            old_price = d["boughtAt"]
            old_token = d["tokens"]
            dca = True
            break
    if dca:
        t1 = old_token * old_price
        t2 = token * price
        tA = t1 - t2
        new_tokens = old_token - token
        if new_tokens != 0:
            dollar_cost_average = tA/new_tokens
            db.owned_crypto.update({'name':context.user_data["name"]}, {"$set":{'boughtAt': dollar_cost_average, 'tokens':new_tokens}})
            update.message.reply_text(f"You sold {name}, your new DCA is ${dollar_cost_average}", reply_markup=markup_default_options)
        else:
            db.owned_crypto.remove({"name":context.user_data["name"]})
            update.message.reply_text(f"You sold {name}, your new DCA is ${dollar_cost_average}.\n You no more own {name}.", reply_markup=markup_default_options)

    else: 
        update.message.reply_text(f"You do not own any {name}!", reply_markup=markup_default_options)
    return SELECTED_OPTION

def help(update:Update, context:CallbackContext): 
    update.message.reply_text('''
    Here is a list of things I can do:
    -- Show OWNED crypto /owned , -- Show PORTFOLIO ,
    -- Show Profit From /profitfrom, -- Show Total Profit /totalprofit ,
    -- Sold tokens, -- Bought tokens,
    ''')

