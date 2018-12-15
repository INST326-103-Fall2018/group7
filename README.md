tweets2csv
==========

https://faizshah.github.io/tweets2csv/

A simple program to pull the last X days tweets from a twitter user's
timeline then either write to a CSV, produce a word cloud, or show a graph of
their likes.

The internal Tweets class uses the twitter frontend timeline api to bypass twitter's rate limiting. As such the program *could* be used to download large amounts of tweets. However, the request rate has been limited internally by a gaussian wait time per request and Tweets have been limited to 31 days to avoid hammering the twitter servers.

The visualizations were produced using pandas, numpy, matplotlib and wordcloud.

Usage:
-----

Simply type:
    
    python3 tweets2csv <twitter_handle> <output_csv> <days>

Optionally, add --cloud and/or --likes to get either a word cloud or some 
info on the user's likes as a graph respectively.
