import unittest
from bs4 import BeautifulSoup
import datetime
import requests
import json
import os

from GroupProject.tweets2csv.src.Tweets import Tweets

class TestTwitterScraper(unittest.TestCase):
    def test_extract_tweet_data(self):
        with open('test_extract.txt','r') as handle:
            html = ''.join(handle.readlines())
        soup = BeautifulSoup(html,'lxml')
        dict = Tweets.extract_tweet_data(soup.select('html > body > li')[0])
        expected = {'tweet_replies': 17161, 'tweet_retweets': 16641,
                 'tweet_likes': 64090,
         'tweet_id': '1073763695807877120',
         'tweet_permalink': '/realDonaldTrump/status/1073763695807877120',
         'tweet_author': 'realDonaldTrump',
         'tweet_author_name': 'Donald J. Trump',
         'tweet_time_epoch_ms': 1544840189000,
         'tweet_date': datetime.datetime(2018, 12, 14, 21, 16, 29),
         'tweet_text': 'Wow, but not surprisingly, ObamaCare was just ruled '
                       'UNCONSTITUTIONAL by a highly respected judge in Texas. '
                       'Great news for America!'}
        self.assertDictEqual(dict,expected)

    def test_extract_tweets(self):
        with open('test_response.txt', 'r') as handle:
            response = handle.readlines()
        extracted = Tweets.extract_tweets(response[0])
        self.assertEqual(len(extracted[0]),20)
        self.assertEqual(extracted[1], '1071939400517500929')

    def test_get_tweets_response(self):
        response = Tweets.get_tweets_response('realdonaldtrump')
        parsed = json.loads(response)
        expected = ['min_position', 'max_position', 'has_more_items',
                    'items_html', 'new_latent_count']
        self.assertEqual(list(parsed.keys()), expected)

    def test_validate_twitter(self):
        invalid = 'fjasbfdj123' * 5
        valid = 'realdonaldtrump'
        self.assertFalse(Tweets.validate_twitter(invalid))
        self.assertTrue(Tweets.validate_twitter(valid))

    def test_csv(self):
        tweets = Tweets('realdonaldtrump', 3)
        self.assertFalse(os.path.isfile('temp_test_file.csv'))
        tweets.to_csv('temp_test_file.csv')
        self.assertTrue(os.path.isfile('temp_test_file.csv'))
        with open('temp_test_file.csv', 'r') as handle:
            lines = handle.readlines()
        self.assertEqual(len(tweets) + 1, len(lines))
        os.remove('temp_test_file.csv')
