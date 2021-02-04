import alpaca_trade_api as tradeapi
import config

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)

def Buy(symbol):
    api.submit_order(symbol, 1, 'buy', 'market', 'day')
    print("Market order submitted.")

def Sell(symbol):
    api.submit_order(symbol, 1, 'sell', 'market', 'day')
    print("Market order submitted.")