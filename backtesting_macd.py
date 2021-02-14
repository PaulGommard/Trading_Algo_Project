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
    try:
        dataDF = data.history(interval='1m', start=GetPastDate(7), end=GetPastDate(0))
        del dataDF['Open']
        del dataDF['Dividends']
        del dataDF['Stock Splits']

        dataDF.reset_index(level=0, inplace=True)
        dataDF.columns = ['Date', 'Close', 'High', 'Low', 'Volume']
        dataDF['e12'] = dataDF.Close.ewm(span=12, adjust=False).mean()
        dataDF['e26'] = dataDF.Close.ewm(span=26, adjust=False).mean()
        dataDF['MACD'] = dataDF['e12'] - dataDF['e26']
        dataDF['e9'] = dataDF['MACD'].ewm(span=9, adjust=False).mean()
        
    except Exception:
        d = {'Date': [0], 'Close': [0],'High': [0], 'Low': [0],'Volume': [0], 'e12': [0],'e26': [0], 'MACD': [0],'e9': [0]}
        dataDF = pd.DataFrame(data=d)

    return dataDF    
    # dataDF = pandas.concat([df1, df2, df3, df4])

    


def BackTestingMACD(df):
    last_order_price = 0    
    last_order = 'sell'
    for row in range(1, len(df)):
        if df.loc[row, 'MACD'] < 0 and df.loc[row - 1, 'MACD'] > 0 and last_order == 'sell': 
            df.loc[row, 'Order'] = 'buy'
            last_order_price = df.loc[row, 'Close']
            last_order = 'buy'
        elif df.loc[row, 'MACD'] > 0 and df.loc[row - 1, 'MACD'] < 0 and last_order_price < df.loc[row, 'Close'] and last_order == 'buy':
            df.loc[row, 'Order'] = 'sell'
            last_order = 'sell'
        else:
            df.loc[row, 'Order'] = 'null'
    
    return df


def CalculateBenef(df):
    benefice = 0
    if(len(df) > 2):
        initial_budget = df.loc[0, 'Close']
        budget = initial_budget
        last_order = "sell"
        last_order_price = 0

        for row in range(1, len(df)):
            if df.loc[row, 'Order'] == 'buy' and last_order == "sell":
                budget = budget - df.loc[row, 'Close']
                last_order = 'buy'
                last_order_price = df.loc[row, 'Close']
            elif df.loc[row, 'Order'] == 'sell' and last_order == "buy": 
                budget = budget + df.loc[row, 'Close']
                last_order = "sell"
        
        if(last_order == 'buy'):
            budget = budget + last_order_price
            
        
        benefice = budget - initial_budget
        benefice = (benefice * 100) / initial_budget

    return benefice

# connection = sqlite3.connect(config.DATA_BASE)
# connection.row_factory = sqlite3.Row
# cursor = connection.cursor()

# cursor.execute("""
#     select id from strategy where name = 'macd'
#     """)

# strategy_id = cursor.fetchone()['id']

# cursor.execute("""
#     select symbol, name
#     from stock
#     join stock_strategy on stock_strategy.stock_id = stock.id
#     where stock_strategy.strategy_id = ?
# """, (strategy_id,))

# stocks = cursor.fetchall()
# symbols = [stock['symbol'] for stock in stocks]


# # for symbol in symbols:
    

# df = GetPastData('IFMK')

# print(BackTestingMACD(df))

# print(CalculateBenef(df))

    
# connection.close()