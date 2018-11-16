import csv


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
