import yfinance as yf
from fastapi import FastAPI, Request
import sqlite3, config
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
from datetime import timedelta


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


connection = sqlite3.connect(config.DATA_BASE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""select distinct stock_id from stock_strategy
    """)
rows = cursor.fetchall()
stocks_id = []

for row in rows:
    stock_id = row['stock_id']
    stocks_id.append(stock_id)


for stock_id in stocks_id:
    cursor.execute("""select symbol from stock where id = (?)
    """, (stock_id,))
    symbol = cursor.fetchone()['symbol']

    last_close = GetActualPrice(symbol)
    now = datetime.now().isoformat()
    cursor.execute("""
    INSERT INTO stock_price_minutes (stock_id, date, close) VALUES (?, ?, ?)
    """, (stock_id, now, last_close,))

    connection.commit()


