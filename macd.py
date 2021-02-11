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

        cursor.execute("""
        select order_statue from order_status_stock where strategy_id = (?) AND stock_id = (?) ORDER BY date DESC
        """, (strategy_id,stock_id),)

        last_order = cursor.fetchone()

        cursor.execute("""
        select last_close from order_status_stock where strategy_id = (?) AND stock_id = (?) ORDER BY date DESC
        """, (strategy_id,stock_id),)

        last_close = cursor.fetchone()
      
        if last_order is None:
            last_order_statue = 'sell'
        else:
            last_order_statue = last_order['order_statue']

        if last_close is None:
            last_close_statue = 0
        else:
            last_close_statue = last_close['last_close']

        row = len(df) - 1
        print(symbol)
        if df.loc[row, 'MACD'] < 0 and df.loc[row - 1, 'MACD'] > 0 and last_order_statue == 'sell':
            submit_orders.Buy(symbol)
            InsertInDataBase("buy", df.loc[row, 'close'])
        elif df.loc[row, 'MACD'] > 0 and df.loc[row - 1, 'MACD'] < 0 and last_order_statue == 'buy' and last_close_statue < df.loc[row, 'close']:
            submit_orders.Sell(symbol)
            InsertInDataBase("sell", df.loc[row, 'close'])


def InsertInDataBase(order_statue, last_close):
    cursor.execute("""
        INSERT INTO order_status_stock (stock_id,strategy_id, date, order_statue, last_close) VALUES (?, ?, ?, ?, ?)
        """, (stock_id, strategy_id, datetime.now(),order_statue, last_close),)

    connection.commit()
        
    
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

    df = pd.read_sql_query(f"""select * from stock_price_minutes where stock_id = ({stock_id}) ORDER BY date ASC""" ,connection)

    ApplyStrategy(symbol)

    connection.commit()


connection.close()
