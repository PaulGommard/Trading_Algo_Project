import alpaca_trade_api as tradeapi
import sqlite3, config


connection = sqlite3.connect(config.DATA_BASE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)
    
def Buy(symbol):
    api.submit_order(
    symbol=symbol,
    qty=1,
    side='buy',
    type='market',
    time_in_force='gtc'
    )
    print("Market buy submitted.")

def Sell(symbol):
    api.submit_order(
    symbol=symbol,
    qty=1,
    side='sell',
    type='market',
    time_in_force='gtc'
    )
    print("Market sell submitted.")
