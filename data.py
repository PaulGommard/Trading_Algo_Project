import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import pandas
from datetime import datetime
from datetime import timedelta
import bs4 as bs
import alpaca_trade_api as tradeapi

# Get the actual price the stock
def GetActualPrice(url):
    try:
        reponse = requests.get(url)
        soup = BeautifulSoup(reponse.text, 'lxml')

        price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
        price = price.replace(u'\xa0', '')
        price = price.replace(',', '.')
        price = price.strip()
        return price

    except:
        print("Error, reboot real time data :")
        time.sleep(2)
        GetActualPrice(url)


# Calculate MACD formule
def GetMACD(dataDF, url):
    dataDF.loc[len(dataDF), 'Close'] = GetActualPrice(url)
    if dataDF.loc[len(dataDF) - 1, 'Close'] == None:
        dataDF.loc[len(dataDF) - 1, 'Close'] = dataDF.loc[len(dataDF) - 2, 'Close']
    dataDF.loc[dataDF.index[len(dataDF) - 1], 'Date'] = time.strftime("%y/%m/%d %H:%M:%S", time.localtime(time.time()))
    dataDF['e12'] = dataDF.Close.ewm(span=12, adjust=False).mean()
    dataDF['e26'] = dataDF.Close.ewm(span=26, adjust=False).mean()
    dataDF['MACD'] = dataDF['e12'] - dataDF['e26']
    dataDF['e9'] = dataDF['MACD'].ewm(span=9, adjust=False).mean()

# Get the date equal to the n days before now
def GetPastDate(days):
    date = str(datetime.now() - timedelta(days=days))
    date = date[0:10]
    return date

# Get 1 month of data of a stock
def GetPastData(ticker):
    sg = ticker
    data = yf.Ticker(sg)

    df1 = data.history(interval='1h', start=GetPastDate(28), end=GetPastDate(21))
    df2 = data.history(interval='1h', start=GetPastDate(21), end=GetPastDate(14))
    df3 = data.history(interval='1h', start=GetPastDate(14), end=GetPastDate(7))
    df4 = data.history(interval='1h', start=GetPastDate(7), end=GetPastDate(0))
    dataDF = pandas.concat([df1, df2, df3, df4])

    del dataDF['Open']
    del dataDF['Dividends']
    del dataDF['Stock Splits']

    dataDF.reset_index(level=0, inplace=True)
    dataDF.columns = ['Date', 'Close', 'High', 'Low', 'Volume']
    dataDF['e12'] = dataDF.Close.ewm(span=12, adjust=False).mean()
    dataDF['e26'] = dataDF.Close.ewm(span=26, adjust=False).mean()
    dataDF['MACD'] = dataDF['e12'] - dataDF['e26']
    dataDF['e9'] = dataDF['MACD'].ewm(span=9, adjust=False).mean()
    print(dataDF)
    # profit = computeStrategy(dataDF)
    # return profit

