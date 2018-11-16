import argparse
import logging
import sys
import os
from scraper import validate_twitter


from tweets2csv import __version__


# validates empty csv file for output
def validate_csv(filename):
    """Examine file that has been entered to ensure it is an empty csv"""

    if filename.endswith('csv'):
        # checks that a file exists and is not blank to the left of the file extension
        dot_position = filename.rfind('.')
        if len(filename[:dot_position] > 0):
            return True
        else:
            raise Exception(f'Invalid Basename. You entered: {OUTPUTFILE}')
    else:
        raise Exception(f'Invalid file extension. You entered: {OUTPUTFILE}')


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
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

    validate_csv(OUTPUTFILE)

    # validates that the csv file entered does not already exist
    if not os.path.exists(OUTPUTFILE):
        sys.exit(f'INVALID FILE: File exists already exists. You entered : {OUTPUTFILE}'
    
    














    #parser = argparse.ArgumentParser(
        #description="Just a Fibonnaci demonstration")
    #parser.add_argument(
        '--version',
        action='version',
        version='tweets2csv {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="n",
        help="n-th Fibonacci number",
        type=int,
        metavar="INT")
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


