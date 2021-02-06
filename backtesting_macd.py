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
import pandas

def GetPastDate(days):
    date = str(datetime.now() - timedelta(days=days))
    date = date[0:10]
    return date

def GetPastData(symbol):
    sg = symbol
    data = yf.Ticker(sg)

    # df1 = data.history(interval='1m', start=GetPastDate(28), end=GetPastDate(21))
    # df2 = data.history(interval='1m', start=GetPastDate(21), end=GetPastDate(14))
    # df3 = data.history(interval='1m', start=GetPastDate(14), end=GetPastDate(7))
    df4 = data.history(interval='1m', start=GetPastDate(1), end=GetPastDate(0))
    # dataDF = pandas.concat([df1, df2, df3, df4])
    dataDF = df4

    del dataDF['Open']
    del dataDF['Dividends']
    del dataDF['Stock Splits']

    dataDF.reset_index(level=0, inplace=True)
    dataDF.columns = ['Date', 'Close', 'High', 'Low', 'Volume']
    dataDF['e12'] = dataDF.Close.ewm(span=12, adjust=False).mean()
    dataDF['e26'] = dataDF.Close.ewm(span=26, adjust=False).mean()
    dataDF['MACD'] = dataDF['e12'] - dataDF['e26']
    dataDF['e9'] = dataDF['MACD'].ewm(span=9, adjust=False).mean()
    return dataDF


def BackTestingMACD(df):
    for row in range(1, len(df)):
        if df.loc[row, 'MACD'] > df.loc[row, 'e9'] and df.loc[row - 1, 'MACD'] < df.loc[row - 1, 'e9']:
            print("BUY")
            print(df.loc[row])
        elif df.loc[row, 'MACD'] < df.loc[row, 'e9'] and df.loc[row - 1, 'MACD'] > df.loc[row - 1, 'e9']:
            print("SELL")
            print(df.loc[row])

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


# for symbol in symbols:
    

df = GetPastData("AAPL")

BackTestingMACD(df)

    
connection.close()