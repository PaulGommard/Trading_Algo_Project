import sqlite3, config
import alpaca_trade_api as tradeapi

# Get the app data already created
connection = sqlite3.connect('app.db')
connection.row_factory = sqlite3.Row

# Create connection
cursor = connection.cursor()

# Get symbol and company from the database
cursor.execute("""SELECT symbol, company FROM stock""")
rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]

# Create connection with Alpaca
api = tradeapi.REST(config.API_KEY,config.SECRET_KEY, base_url=config.BASE_URL)
assets = api.list_assets()

# Insert the new stock in the db
for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable:
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)


connection.commit()