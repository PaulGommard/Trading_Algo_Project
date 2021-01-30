import config
import alpaca_trade_api as tradeapi
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)
    
barsets = api.get_barset(['AAPL', 'MSFT'], 'minute')
# loop over the keys in the barsets dictionary
for symbol in barsets:
    print(f"processing symbol {symbol}")
    
    # loop through each bar for the current symbol in the dictionary
    for bar in barsets[symbol]:
        print(bar.t, bar.o, bar.h, bar.l, bar.c, bar.v)  