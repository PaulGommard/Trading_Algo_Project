import sqlite3

connection = sqlite3.connect('app.db')

cursor = connection.cursor()

# Stock table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock ( 
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL
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

connection.commit()

