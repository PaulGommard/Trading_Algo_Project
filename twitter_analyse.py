from textblob import TextBlob
import tweepy
import sys
from donnees import *

auth_handler = tweepy.OAuthHandler(consumer_key=api_key,consumer_secret=api_key_secret)
auth_handler.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth_handler)

search_term = 'bitcoin'

tweet_amount = 200

tweets = tweepy.Cursor(api.search, q=search_term, lang='en').items(tweet_amount)
polarity = 0
positive = 0
neutral = 0
negative = 0

for tweet in tweets:
    final_text = tweet.text.replace('RT', '')
    if final_text.startswith(' @'):
        position = final_text.index(':')
        final_text = final_text[position+2:]
    if final_text.startswith('@'):
        position = final_text.index(' ')
        final_text = final_text[position+2:]
    analysis = TextBlob(final_text)
    tweet_polarity = analysis.polarity
    if(tweet_polarity > 0):
        positive += 1
        print("Positive ----------------------------------------------------------------------------------")
        print(final_text)
    elif(tweet_polarity < 0):
        negative += 1
        print("NEGATIVE ----------------------------------------------------------------------------------")
        print(final_text)
    else:
        neutral += 1
        print("NEUTRAL ----------------------------------------------------------------------------------")
        print(final_text)
    polarity += tweet_polarity


print(f"Positive : {positive}")
print(f"Neutral : {neutral}")
print(f"Negative : {negative}")

