import argparse
import logging
import sys
import os
from .scraper import validate_twitter

from unittest import TestCase as tc

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
        raise Exception(f' Invalid file extension. You entered {OUTPUTFILE}')

    if filename.endswith(extension):
        # checks that a file exists and is not blank to the left of the file extension
        dot_position = filename.rfind('.')
        if len(filename[:dot_position]) > 0:
            return True
        else:
            raise Exception(f'Invalid Basename. You entered: {OUTPUTFILE}')
    else:
        raise Exception(f'Invalid file extension. You entered: {OUTPUTFILE}')


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

    args = parser.parse_args()
    TWITTERHANDLE = args.twitter_handle
    OUTPUTFILE = args.output_csv

    # validating the arguments
    if not validate_twitter(TWITTERHANDLE):
        raise ValueError(f'The input Twitter handle is not valid. You entered : {TWITTERHANDLE}')

    validate_file(OUTPUTFILE,'csv')

    # validates that the csv file entered does not already exist
    if os.path.exists(OUTPUTFILE):
        sys.exit(f'INVALID FILE: File exists already exists. You entered : '
                 f'{OUTPUTFILE}')

    return {"twitterhandle":TWITTERHANDLE, "outputfile":OUTPUTFILE}


if __name__ == '__main__':
    # test for validate file
    tc.assertFalse(validate_file('','csv'))
    tc.assertFalse(validate_file('.csv', 'csv'))
    tc.assertFalse(validate_file('filename.', ''))
    tc.assertTrue(validate_file('filename.', 'csv'))

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






