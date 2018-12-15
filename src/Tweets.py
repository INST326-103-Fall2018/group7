#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Name: Group 7
# Date: 2018-12-14
# Assignment: Group Project

from twitter_scraper import get_tweets
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from operator import itemgetter
from datetime import datetime, timedelta
import time
import random
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

class Tweets(list):

    # Author: Faiz
    @staticmethod
    def extract_tweet_data(list_item):
        '''
        Given a list item from the tweet list, extract the data and return it as
        a dictionary.

        :param list_item:
            A beautiful soup li element for a tweet.
        :return:
            A dictionary of the tweet's data.
        '''

        tweet_dict = {}

        tweet_action_counts_raw = \
            list_item.select('.ProfileTweet-actionCountList'
                             ' > span > .ProfileTweet-actionCount')
        tweet_metadata_attrs = list_item.select('.tweet')[0].attrs

        tweet_action_counts = \
            [z.attrs.get('data-tweet-stat-count') for z in
             tweet_action_counts_raw]
        tweet_metadata = itemgetter('data-tweet-id', 'data-permalink-path',
                                    'data-screen-name', 'data-name')(
            tweet_metadata_attrs)

        [tweet_dict['tweet_replies'],
         tweet_dict['tweet_retweets'],
         tweet_dict['tweet_likes']] = [int(c) for c in tweet_action_counts]

        (tweet_dict['tweet_id'], tweet_dict['tweet_permalink'], tweet_dict[
            'tweet_author'], tweet_dict['tweet_author_name']) = tweet_metadata

        tweet_dict['tweet_time_epoch_ms'] = \
            int(list_item.select('._timestamp')[0].attrs['data-time-ms'])
        tweet_dict['tweet_date'] = \
            datetime.fromtimestamp(tweet_dict['tweet_time_epoch_ms'] / 1000)
        tweet_dict['tweet_text'] = \
            ' '.join(list_item.select('.tweet-text')[0].find_all(text=True))

        return tweet_dict

    # Author: Faiz
    @staticmethod
    def extract_tweets(response_text):
        '''
        Given the json response, return a list of dictionaries containing the
        tweets data and the min_position value.

        :param response_text:
            Json response text from timeline.
        :return:
            A list of dictionaries of tweets data and the min_position.
        '''
        tweets = []
        parsed_response = json.loads(response_text)
        soup = BeautifulSoup(parsed_response['items_html'], 'lxml')
        tweets_html_list = soup.select('body > li')
        for tweet_element in tweets_html_list:
            tweets.append(Tweets.extract_tweet_data(tweet_element))
        return (tweets, parsed_response['min_position'])

    # Author: Faiz
    @staticmethod
    def get_tweets_response(twitter_user, max_position = 0):
        '''
        Given a twitter user and max position, return the text response from
        the twitter timeline endpoint.

        :param twitter_user:
            Twitter user handle, no @.
        :param max_position:
            Max position, if this is your first request use a number less
            than 1 or use the default.
        :return:
            The text response.
        '''
        url = f'https://twitter.com/i/profiles/show/{twitter_user}/' \
              f'timeline/tweets'
        if int(max_position) > 0:
            url += f'?max_position={max_position}'
        response = requests.get(url)
        text = response.text
        return text

    # Author: Faiz
    @staticmethod
    def scrape_tweets(twitter_user, days):
        '''
        Given a twitter handle and a number of days, return all the tweets
        from the number of responses necessary to reach the day limit.

        :param twitter_user:
            A twitter handle, no @ sign.
        :param days:
            A integer number of days.
        :return:
            A list of tweets that is a multiple of 20 containing the desired
            interval of tweets (including some tweets outside of the desired
            interval).
        '''
        cur_date = datetime.now()
        end_date = cur_date - timedelta(days=days)
        max_position = 0
        tweets_collected = []
        while end_date < cur_date:
            response_text = Tweets.get_tweets_response(twitter_user,
                                                      max_position)
            tweets, max_position = Tweets.extract_tweets(response_text)
            tweets_collected.extend(tweets)
            cur_date = tweets_collected[-1]['tweet_date']
            # To avoid hammering the server.
            time.sleep(abs(random.gauss(1, 0.5)) * 2)
        return tweets_collected

    # Author: Faiz
    @staticmethod
    def validate_twitter(twitter_handle):
        '''
        Validate that a twitter handle exists using twitters internal api.

        :param twitter_handle:
            The twitter handle, no @.
        :return:
            True if the handle exists else false.
        '''
        response = requests.get(f'https://twitter.com/users/username_available'
                                f'?username={twitter_handle}')
        message = json.loads(response.text)
        return not message['valid']

    # Author: Faiz
    def __init__(self, twitter_handle, days = 7):
        # For our purposes you should never go above 31 days.
        days = min(days, 31)
        end_date = datetime.now() - timedelta(days=days)
        tweets = Tweets.scrape_tweets(twitter_handle, days)
        for x in tweets:
            if x['tweet_date'] < end_date:
                break
            else:
                self.append(x)

    # Author: Joe
    def to_csv(self, outputfile):
        '''This function intakes a list of tweets and outputs a csv

        :param tweets:

        This is a list of dictionarys for tweets

        :param outputfile:

        The name of a csv file that does not exist'''

        with open(outputfile, 'w') as handle:
            tweets = self
            writer = csv.writer(handle)
            # writer.writeheader()
            writer.writerow(tweets[0].keys())
            for tweet in tweets:
                writer.writerow(tweet.values())

    # Author: Joe
    def tweets_info(self):
        '''
        Show info of most and least liked tweets.
        '''
        tweets = self
        # puts tweets in DF
        data = pd.DataFrame(data=[tweet for tweet in tweets], columns=tweets[0])
        # prints least and most number of likes
        max_likes = np.max(data.tweet_likes)
        print('Most likes is {0}'.format(max_likes))
        min_likes = np.min(data.tweet_likes)
        print('Least likes is {0}'.format(min_likes))
        # shows likes over time
        tfav = pd.Series(data=data.tweet_likes.values,
                         index=data.tweet_time_epoch_ms)
        tfav.plot(figsize=(16, 4), color='r')
        plt.show()

    # Author: Joe
    def tweet_cloud(self):
        '''
        Generate a word cloud for our tweets.
        '''
        tweets = self
        # tweets in DF
        data = pd.DataFrame(data=[tweet for tweet in tweets], columns=tweets[0])
        # filtering down to just words without special chars
        words = ' '.join(data.tweet_text)
        no_urls = " ".join([word for word in words.split()
                            if 'http' not in word
                            and not word.startswith('@')
                            and word != 'RT'
                            ])
        # Makes word cloud
        wordcloud = WordCloud(stopwords=STOPWORDS,
                              background_color='black').generate(no_urls)
        plt.imshow(wordcloud)
        plt.axis('off')
        # prints the cloud
        plt.show()

