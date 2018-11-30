#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Name: Faiz Shah
# Directory ID: faizshah
# Date: 2018-11-11
# Assignment: Exam 2, Take-Home Question 1

from twitter_scraper import get_tweets
import json
import requests

def scrape_tweets(twitter_handle, days):
    tweets = get_tweets(twitter_handle, days)
    return list(tweets)

def validate_twitter(twitter_handle):
    response = requests.get(f'https://twitter.com/users/username_available'
                       f'?username={twitter_handle}')
    message = json.loads(response.text)
    return not message['valid']