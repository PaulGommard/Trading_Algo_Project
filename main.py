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
import data

df =  pd.DataFrame(columns=['Close', 'e9', 'MACD', 'e26', 'lastClose', 'e12', 'Position'])
url_TEL = 'https://fr.finance.yahoo.com/quote/TEL?p=TEL'


# Get the actual price the stock
def actual_price(url):
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
        actual_price(url)


# Calculate MACD formule
def get_MACD_data(dataDF, url):
    dataDF.loc[len(dataDF), 'Close'] = actual_price(url)
    if dataDF.loc[len(dataDF) - 1, 'Close'] == None:
        dataDF.loc[len(dataDF) - 1, 'Close'] = dataDF.loc[len(dataDF) - 2, 'Close']
    dataDF.loc[dataDF.index[len(dataDF) - 1], 'Date'] = time.strftime("%y/%m/%d %H:%M:%S", time.localtime(time.time()))
    dataDF['e12'] = dataDF.Close.ewm(span=12, adjust=False).mean()
    dataDF['e26'] = dataDF.Close.ewm(span=26, adjust=False).mean()
    dataDF['MACD'] = dataDF['e12'] - dataDF['e26']
    dataDF['e9'] = dataDF['MACD'].ewm(span=9, adjust=False).mean()


def get_past_date(days):
    date = str(datetime.now() - timedelta(days=days))
    date = date[0:10]
    return date

def get_past_data(ticker):
    sg = ticker
    data = yf.Ticker(sg)

    df1 = data.history(interval='1h', start=get_past_date(28), end=get_past_date(21))
    df2 = data.history(interval='1h', start=get_past_date(21), end=get_past_date(14))
    df3 = data.history(interval='1h', start=get_past_date(14), end=get_past_date(7))
    df4 = data.history(interval='1h', start=get_past_date(7), end=get_past_date(0))
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
    #profit = computeStrategy(dataDF)
    #return profit
    plt.subplot(2, 1, 1)
    plt.plot(dataDF['Date'],dataDF['Close'])
    plt.subplot(2, 1, 2)
    plt.plot(dataDF['Date'], dataDF['MACD'])
    plt.plot(dataDF['Date'], dataDF['e9'])
    plt.show()




get_past_data("AAPL")

print(actual_price(url_TEL))

