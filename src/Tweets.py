import csv
from .scraper import scrape_tweets
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def to_csv(tweets, outputfile):
    '''This function intakes a list of tweets and outputs a csv

    :param tweets:

    This is a list of dictionarys for tweets

    :param outputfile:

    The name of a csv file that does not exist'''

    with open(outputfile, 'w') as handle:
        writer = csv.writer(handle)
        # writer.writeheader()
        writer.writerow(tweets[0].keys())
        for tweet in tweets:
            writer.writerow(tweet.values())

tweets = scrape_tweets('@realDonaldTrump', 1)


def tweets_info(tweets):
    # puts tweets in DF
    data = pd.DataFrame(data=[tweet for tweet in tweets], columns=tweets[0])
    # prints least and most number of likes
    max_likes = np.max(data.likes)
    print('Most likes is {0}'.format(max_likes))
    min_likes = np.min(data.likes)
    print('Least likes is {0}'.format(min_likes))
    # shows likes over time
    tfav = pd.Series(data=data.likes.values, index=data.time)
    tfav.plot(figsize=(16, 4), color='r')
    plt.show()


def tweet_cloud(tweets):
    #tweets in DF
    data = pd.DataFrame(data=[tweet for tweet in tweets], columns=tweets[0])
    # filtering down to just words without special chars
    words = ' '.join(data.text)
    no_urls = " ".join([word for word in words.split()
                        if 'http' not in word
                        and not word.startswith('@')
                        and word != 'RT'
                        ])
    # Makes word cloud
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='black').generate(no_urls)
    plt.imshow(wordcloud)
    plt.axis('off')
    # prints the cloud
    plt.show()
