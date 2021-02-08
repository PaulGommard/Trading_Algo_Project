import yfinance as yf
from datetime import datetime
from datetime import timedelta
import pandas as pd
from fastapi import FastAPI, Request
import sqlite3, config
import alpaca_trade_api as tradeapi
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import submit_orders

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)

def ApplyStrategy(symbol):
    if(len(df) > 26):
        df['e12'] = df.close.ewm(span=12, adjust=False).mean()
        df['e26'] = df.close.ewm(span=26, adjust=False).mean()
        df['MACD'] = df['e12'] - df['e26']
        df['e9'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    row = len(df) - 1
    if df.loc[row, 'MACD'] > df.loc[row, 'e9'] and df.loc[row - 1, 'MACD'] < df.loc[row - 1, 'e9'] and df.loc[row, 'MACD'] < 0:
        submit_orders.Buy(symbol)
    elif df.loc[row, 'MACD'] < df.loc[row, 'e9'] and df.loc[row - 1, 'MACD'] > df.loc[row - 1, 'e9']:
        submit_orders.Sell(symbol)
        
    
connection = sqlite3.connect(config.DATA_BASE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    select id from strategy where name = 'macd'
    """)

strategy_id = cursor.fetchone()['id']

cursor.execute("""
    select symbol, name
    from stock
    join stock_strategy on stock_strategy.stock_id = stock.id
    where stock_strategy.strategy_id = ?
""", (strategy_id,))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]


for symbol in symbols:
    cursor.execute("""select * from stock where symbol = (?)
    """, (symbol,))
    stock_id = cursor.fetchone()['id']

    df = pd.read_sql_query(f"""select * from stock_price_minutes where stock_id = ({stock_id}) ORDER BY date DESC""" ,connection)
    print(df)

    ApplyStrategy(symbol)

    connection.commit()

    
connection.close()
""" data = yf.Ticker(symbol)
    df = data.history(interval='1m', start=GetPastDate(7), end=GetPastDate(0))
    print(df) """