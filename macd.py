import yfinance as yf
from datetime import datetime
from datetime import timedelta
import pandas
from fastapi import FastAPI, Request
import sqlite3, config
import alpaca_trade_api as tradeapi
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)

# Get the date equal to the n days before now
def GetPastDate(days):
    date = str(datetime.now() - timedelta(days=days))
    date = date[0:10]
    return date

# Get the actual price the stock
def GetActualPrice(symbol):
    try:
        url = f'https://fr.finance.yahoo.com/quote/{symbol}?p=ABT'
        reponse = requests.get(url)
        soup = BeautifulSoup(reponse.text, 'lxml')

        price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
        price = price.replace(u'\xa0', '')
        price = price.replace(',', '.')
        price = price.strip()
        return price

    except:
        print(f"Don't find the price for {symbol}")
        time.sleep(2)
        GetActualPrice(symbol)

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
    close = GetActualPrice(symbol)
    now = datetime.now().isoformat()
    print(symbol)
    cursor.execute("""select * from stock where symbol = (?)
    """, (symbol,))
    stock_id = cursor.fetchone()['id']
    
    cursor.execute("""
    INSERT INTO stock_price_minutes (stock_id, date, close) VALUES (?, ?, ?)
    """, (stock_id, now, close,))

    connection.commit()
    
    # data = yf.Ticker(symbol)
    # df = data.history(interval='1m', start=GetPastDate(7), end=GetPastDate(0))
    # print(df)
    

