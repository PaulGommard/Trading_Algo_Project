import sqlite3, config
import alpaca_trade_api as tradeapi

connection = sqlite3.connect('app.db')
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""SELECT symbol, company FROM stock""")
rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]


api = tradeapi.REST(config.API_KEY,config.SECRET_KEY, base_url=config.BASE_URL)
assets = api.list_assets()

def GetListStocks():
    for asset in assets:
        try:
            if asset.status == 'active' and asset.tradable:
                print(f"Added a new stock {asset.symbol} {asset.name}")
                cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
        except Exception as e:
            print(asset.symbol)
            print(e)

GetListStocks()

connection.commit()