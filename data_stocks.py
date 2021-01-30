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
    return dataDF
    # profit = computeStrategy(dataDF)
    # return profit

def computeStrategy(df):
    move = 'buy'  # drapeau qui servira à signaler le prochain mouvement 'buy' > 'sell' > 'buy' etc...

    # crée des colonnes vides dans laquelle nous placerons notre strategie et notre budget
    df['Position'] = None
    df['Budget'] = 5000

    premier_achat = 0
    dernier_budget = 0
    budget_base = 0
    close_base = 1

    for row in range(1, len(df)):
        date = str(df.loc[row, 'Date'])
        # conditions pour un achat
        if df.loc[row, 'MACD'] > df.loc[row, 'e9'] and df.loc[row - 1, 'MACD'] < df.loc[row, 'e9'] and df.loc[
            row, 'MACD'] < 0 and move == 'buy':
            df.loc[row, 'Position'] = 'buy'
            move = 'sell'
            lastClose = df.loc[row, 'Close']
            if premier_achat == 0:
                close_base = df.loc[row, 'Close']
                budget_base = df.loc[row, 'Budget']
            df.loc[row, 'Budget'] = df.loc[row - 1, 'Budget'] - df.loc[row, 'Close'] - (0.002 * df.loc[row, 'Close'])
            print(df.loc[row])
            order = 'buy'
            # submit_orders(order)
            premier_achat = 1
        # conditions pour une vente
        elif df.loc[row, 'MACD'] < df.loc[row, 'e9'] and df.loc[row - 1, 'MACD'] > df.loc[
            row, 'e9'] and move == 'sell' and df.loc[row, 'Close'] > lastClose:
            df.loc[row, 'Position'] = 'sell'
            move = 'buy'
            df.loc[row, 'Budget'] = df.loc[row - 1, 'Budget'] + df.loc[row, 'Close'] - (0.002 * df.loc[row, 'Close'])
            dernier_budget = df.loc[row, 'Budget']
            order = 'sell'
            # submit_orders(order)
            print(df.loc[row])
        # ni vente ni achat, nous tenons la position
        elif date[11:25] == "15:58:0f-04:00" and move == 'sell':
            df.loc[row, 'Position'] = 'sell'
            move = 'buy'
            df.loc[row, 'Budget'] = df.loc[row - 1, 'Budget'] + df.loc[row, 'Close']
            dernier_budget = df.loc[row, 'Budget']
            order = 'sell'
            # submit_orders(order)
            # print(df.loc[row])
        else:
            df.loc[row, 'Position'] = 'hold'
            df.loc[row, 'Budget'] = df.loc[row - 1, 'Budget']
    profit = (100 * (dernier_budget - budget_base)) / close_base
    profit = round(profit, 2)
    # print('Profit : ' + str(profit) + '%')
    return profit
