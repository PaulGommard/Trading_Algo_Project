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


print(data.GetActualPrice(url_TEL))

