import tweepy as tw
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sys
from donnees import *
from textblob import TextBlob
import datetime

auth_handler = tw.OAuthHandler(consumer_key=api_key,consumer_secret=api_key_secret)
auth_handler.set_access_token(access_token,access_token_secret)

api = tw.API(auth_handler)

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


hashtag = "TSLA"
query = tw.Cursor(api.search, q=hashtag).items(100)

tweets = [{'Tweet':tweet.text, 'Timestamp':tweet.created_at, "Polarity":GetPolarity(tweet)} for tweet in query]

df = pd.DataFrame.from_dict(tweets)
df.head()

df['Timestamp'] = pd.to_datetime(df['Timestamp'])

print(df)

data = pd.DataFrame(columns=["Timestamp","Tweet","Polarity"])

endDate = df.loc[0,'Timestamp']
startDate = endDate - datetime.timedelta(minutes=1)

print(endDate)
print(startDate)

for d in df.itertuples():
    if(d.Timestamp > startDate) and d.Timestamp < endDate:
        data.loc[len(data)] = [d.Timestamp, d.Tweet, d.Polarity]

print(data)
print(data['Polarity'].sum())
print(len(data))

# for time in df['Timestamp']:
#     if(time > datetime.datetime.now() - datetime.timedelta(hours=1,minutes=1)):
        


# for query in querys:
#     final_text = query.text.replace('RT', '')

#     if final_text.startswith(' @'):
#         position = final_text.index(':')
#         final_text = final_text[position+2:]

#     if final_text.startswith('@'):
#         position = final_text.index(' ')
#         final_text = final_text[position+2:]

#     analysis = TextBlob(final_text)
#     tweet_polarity = analysis.polarity
#     # print(tweet_polarity)


# trump_handle = ['DonaldTrump', 'Donald Trump', 'Donald', 'Trump', 'Trump\'s']
# biden_handle = ['JoeBiden', 'Joe Biden', 'Joe', 'Biden', 'Biden\'s']


# def identify_subject(tweet, refs):
#     flag = 0 
#     for ref in refs:
#         if tweet.find(ref) != -1:
#             flag = 1
#     return flag

# df['Trump'] = df['Tweet'].apply(lambda x: identify_subject(x, trump_handle)) 
# df['Biden'] = df['Tweet'].apply(lambda x: identify_subject(x, biden_handle))
# df.head(10)

# # Import stopwords
# import nltk
# from nltk.corpus import stopwords

# # Import textblob
# from textblob import Word, TextBlob


# nltk.download('stopwords')
# nltk.download('wordnet')
# stop_words = stopwords.words('english')
# custom_stopwords = ['RT', '#PresidentialDebate']

# def preprocess_tweets(tweet, custom_stopwords):
#     processed_tweet = tweet
#     processed_tweet.replace('[^\w\s]', '')
#     processed_tweet = " ".join(word for word in processed_tweet.split() if word not in stop_words)
#     processed_tweet = " ".join(word for word in processed_tweet.split() if word not in custom_stopwords)
#     processed_tweet = " ".join(Word(word).lemmatize() for word in processed_tweet.split())
#     return(processed_tweet)

# df['Processed Tweet'] = df['Tweet'].apply(lambda x: preprocess_tweets(x, custom_stopwords))
# df.head()

# print('Base review\n', df['Tweet'][0])
# print('\n------------------------------------\n')
# print('Cleaned and lemmatized review\n', df['Processed Tweet'][0])

# # Calculate polarity
# df['polarity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[0])
# df['subjectivity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[1])
# df[['Processed Tweet', 'Biden', 'Trump', 'polarity', 'subjectivity']].head()


# df[df['Biden']==1][['Biden','polarity','subjectivity']].groupby('Biden').agg([np.mean, np.max, np.min, np.median])

# biden = df[df['Biden']==1][['Timestamp', 'polarity']]
# biden = biden.sort_values(by='Timestamp', ascending=True)
# biden['MA Polarity'] = biden.polarity.rolling(10, min_periods=3).mean()

# trump = df[df['Trump']==1][['Timestamp', 'polarity']]
# trump = trump.sort_values(by='Timestamp', ascending=True)
# trump['MA Polarity'] = trump.polarity.rolling(10, min_periods=3).mean()

# trump.head()

# repub = 'red'
# demo = 'blue'
# fig, axes = plt.subplots(2, 1, figsize=(13, 10))

# axes[0].plot(biden['Timestamp'], biden['MA Polarity'])
# axes[0].set_title("\n".join(["Biden Polarity"]))
# axes[1].plot(trump['Timestamp'], trump['MA Polarity'], color='red')
# axes[1].set_title("\n".join(["Trump Polarity"]))

# fig.suptitle("\n".join(["Presidential Debate Analysis"]), y=0.98)

# plt.show()
