from fastapi import FastAPI, Request
import sqlite3, config
from datetime import datetime
import time
import requests
import tweepy as tw
import numpy as np
import pandas as pd
import sys
from donnees import *
from textblob import TextBlob
import datetime

auth_handler = tw.AppAuthHandler(api_key, api_key_secret)
# auth_handler.set_access_token(access_token,access_token_secret)

api = tw.API(auth_handler, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def GetPolarity(tweet):
    final_text = tweet.text.replace('RT', '')

    if final_text.startswith(' @'):
        position = final_text.index(':')
        final_text = final_text[position+2:]

    if final_text.startswith('@'):
        position = final_text.index(' ')
        final_text = final_text[position+2:]

    analysis = TextBlob(final_text)
    tweet_polarity = analysis.polarity
    return tweet_polarity



def GetData(symnol):
    hastag = f'#{symbol}'
    print(hastag)
    query = tw.Cursor(api.search, q=symbol, lang='en').items(100)

    tweets = [{'Tweet':tweet.text, 'Timestamp':tweet.created_at, "Polarity":GetPolarity(tweet)} for tweet in query]

    df = pd.DataFrame.from_dict(tweets)
    df.head()
    print(symbol)
    print(df)

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    data = pd.DataFrame(columns=["Timestamp","Tweet","Polarity"])

    endDate = datetime.datetime.now()- datetime.timedelta(hours=1)
    startDate = endDate - datetime.timedelta(hours=1, minutes=20)

    for d in df.itertuples():
        if(d.Timestamp > startDate) and d.Timestamp < endDate:
            data.loc[len(data)] = [d.Timestamp, d.Tweet, d.Polarity]
    return data



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

    data = GetData(symbol)

    polarity_sum = data['Polarity'].sum()
    volume = len(data)
    date = datetime.datetime.now()- datetime.timedelta(minutes=20)

    cursor.execute("""
        INSERT INTO twitter_analysis (stock_id, date, polarity, volume) VALUES (?, ?, ?, ?)
    """, (stock_id, date, polarity_sum, volume))

    connection.commit()


connection.close()