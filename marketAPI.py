from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from decouple import config
import json


def get_current_price(token):
    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
    parameters = {
        "amount":"1",
        "symbol": token
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config('COINMARKET_API_KEY')
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        res = json.loads(response.text)
        current_price = res["data"]["quote"]["USD"]["price"]
        return current_price
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return exit
