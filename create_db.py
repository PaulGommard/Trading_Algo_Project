import sqlite3

connection = sqlite3.connect('app.db')

cursor = connection.cursor()

# Stock table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock ( 
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        exchange TEXT NOT NULL
    )
""")
# Stock_price table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_price ( 
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER, 
        date NOT NULL, 
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL,
        close NOT NULL, 
        volume NOT NULL, 
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS strategy ( 
        id INTEGER PRIMARY KEY,
        name NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_strategy ( 
        stock_id INTEGER NOT NULL,
        strategy_id INTEGER NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
        FOREIGN KEY (strategy_id) REFERENCES strategy (id)
    )
""")

strategies = ['macd']

# for strategy in strategies:
#     cursor.execute("""
#     INSERT INTO strategy (name) VALUES (?)
#     """, (strategy,))

connection.commit()

