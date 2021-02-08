import yfinance as yf
import pandas as pd
from fastapi import FastAPI, Request
import sqlite3, config
import alpaca_trade_api as tradeapi
import time
import requests
from bs4 import BeautifulSoup
from datetime import date

import submit_orders
import pandas
import backtesting_macd

# Get the app data already created
connection = sqlite3.connect(config.DATA_BASE)
connection.row_factory = sqlite3.Row

# Create connection
cursor = connection.cursor()

# Get symbol and company from the database
cursor.execute("""SELECT symbol, name, id FROM stock ORDER by symbol""")

rows = cursor.fetchall()

for row in rows:
    df = backtesting_macd.GetPastData(row['symbol'])
    df = backtesting_macd.BackTestingMACD(df) 
    benefice = backtesting_macd.CalculateBenef(df)

    date = pd.to_datetime(df.loc[0, 'Date']).date()

    try:
        cursor.execute("""INSERT INTO backtesting_macd (stock_id, date, benefice, volume_order)
        VALUES (?,?,?,?)
        """, (row['id'], date, benefice, len(df),))
    except:
        cursor.execute("""INSERT INTO backtesting_macd (stock_id, date, benefice, volume_order)
        VALUES (?,?,?,?)
        """, (row['id'], date, 0, 0,))

    connection.commit()
