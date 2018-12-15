#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import logging

from .cli import parse_args
from .Tweets import Tweets

def main(args):
    """
    Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    tweets = Tweets(args['twitterhandle'], args['days'])
    if(args['cloud']):
        tweets.tweet_cloud()
    if(args['likes']):
        tweets.tweets_info()
    tweets.to_csv(args['outputfile'])

def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
