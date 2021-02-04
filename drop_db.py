import sqlite3
import config

connection = sqlite3.connect(config.DATA_BASE)

cursor = connection.cursor()

cursor.execute("""
    DROP TABLE stock_price
    """)

cursor.execute("""
    DROP TABLE stock
    """)

connection.commit()