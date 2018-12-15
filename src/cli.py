import argparse
import logging
import sys
import os
from .Tweets import Tweets

from unittest import TestCase as tc

# Author: Meagan
def validate_file(filename, extension):
    """
    Examine file that has been entered to ensure it is a valid filename for a
    particular file extension.

    :param filename:
        The filename to test.
    :param extension:
        The extension to test that appears AFTER THE LAST '.'
    :return:
        True if valid filename with extension. False if not valid filename
        with extension.
    """
    if extension == '':
        raise Exception(f' Invalid file extension. You entered {filename}')

    if filename.endswith(extension):
        # checks that a file exists and is not blank to the left of the file extension
        dot_position = filename.rfind('.')
        if len(filename[:dot_position]) > 0:
            return True
        else:
            raise Exception(f'Invalid Basename. You entered: {filename}')
    else:
        raise Exception(f'Invalid file extension. You entered: {filename}')

# Author: Meagan
def parse_args(args):
    """
    Parsed command line arguments into variables.

    :param args:
        The array of command line arguments from stdin.
    :return:
        The parsed arguments as a dictionary {twitterhandle, outputfile}
    """


    parser = argparse.ArgumentParser(args)

    # collecting the arguments
    parser.add_argument('twitter_handle')
    parser.add_argument('output_csv')
    parser.add_argument('days')
    parser.add_argument('--cloud', nargs='?', default=False, const=True)
    parser.add_argument('--likes', nargs='?', default=False, const=True)

    args = parser.parse_args()
    TWITTERHANDLE = args.twitter_handle
    OUTPUTFILE = args.output_csv
    try:
        DAYS = int(args.days)
    except:
        sys.exit(f'Please enter a valid integer for the number of days. You '
                f'entered: {args.days}')

    # validating the arguments
    if not Tweets.validate_twitter(TWITTERHANDLE):
        sys.exit(f'The input Twitter handle is not valid. You entered : ' \
          '{TWITTERHANDLE}')

    validate_file(OUTPUTFILE,'csv')

    # validates that the csv file entered does not already exist
    if os.path.exists(OUTPUTFILE):
        sys.exit(f'INVALID FILE: File exists already exists. You entered : '
                 f'{OUTPUTFILE}')

    if DAYS < 1 :
        sys.exit(f'INVALID DAYS: Days must be a positive integer! You '
                 f'entered: {DAYS}')

    return {"twitterhandle":TWITTERHANDLE, "outputfile":OUTPUTFILE, "days":
        DAYS, "cloud": args.cloud, "likes": args.likes}


if __name__ == '__main__':
    # test for validate file
    with tc.assertRaises(expected_exception=Exception,self=tc):
        validate_file('', 'csv')
    with tc.assertRaises(expected_exception=Exception,self=tc):
        validate_file('.csv', 'csv')
    with tc.assertRaises(expected_exception=Exception,self=tc):
        validate_file('filename.', '')
    with tc.assertRaises(expected_exception=Exception,self=tc):
        validate_file('filename.csv', 'csv')

    valid_case = ['realdonaldtrump', 'test.csv']
    # test for parse_args
    tc.assertRaises(ValueError, parse_args(['zxcvbnmasdfghjklqwertyuiop', 'test.csv']))
    with tc.assertRaises(SystemExit):
        # create the file
        with open('test.csv', 'w') as empty_csv:
            pass
        parse_args(['realdonaldtrump', 'test.csv'])
        # delete the file
        os.remove('test.csv')
    tc.assertEqual({"twitterhandle":valid_case[0], "outputfile":valid_case[1]},parse_args(valid_case))






