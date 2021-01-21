from textwrap import TextBlob
import tweepy
import sys
from donnees import *

auth_handler = tweepy.OAuthHandler(consumer_key=api_key, consumer_key=api_key_secret)
auth_handler.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth_handler)

search_term = 'stocks'

tweet_amout = 200

tweets = tweepy.Cursor(api.search, q=search_term, lang='en').items(tweet_amout)

for tweet in tweets:
    print(tweets.text)
