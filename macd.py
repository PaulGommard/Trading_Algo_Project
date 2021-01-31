import yfinance as yf
from datetime import datetime
from datetime import timedelta
import pandas
from fastapi import FastAPI, Request, Form
import sqlite3, config
from fastapi.templating import Jinja2Templates
from datetime import date
from fastapi.responses import RedirectResponse

# Get the date equal to the n days before now
def GetPastDate(days):
    date = str(datetime.now() - timedelta(days=days))
    date = date[0:10]
    return date

connection = sqlite3.connect('app.db')
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
    



sg = 'AAPL'
data = yf.Ticker(sg)

df1 = data.history(interval='1m', start=GetPastDate(7), end=GetPastDate(0))

dataDF = pandas.concat([df1])

# print(df1)

