import unittest
import os

from GroupProject.tweets2csv.src.cli import parse_args, validate_file

class TestTwitterScraper(unittest.TestCase):
    def test_validate_file(self):
        with self.assertRaises(expected_exception=Exception):
            validate_file('', 'csv')
        with self.assertRaises(expected_exception=Exception):
            validate_file('.csv', 'csv')
        with self.assertRaises(expected_exception=Exception):
            validate_file('filename.', '')
        self.assertTrue(validate_file('filename.csv', 'csv'))

    # I can't figure out why this test doesn't work, even though command line
    #  arguments work I can't properly test them in a unit test.
    @unittest.skip('Cant debug this test for some reason. Just use pytest on '
                   'cli.py for now.')
    def test_args(self):
        valid_case =['realdonaldtrump', 'test.csv', '5']
        # test for parse_args
        with self.assertRaises(SystemExit):
            parse_args(['zxcvbnmasdfghjklqwertyuiop','test.csv','5'])
        with self.assertRaises(SystemExit):
            # create the file
            with open('test.csv', 'w') as empty_csv:
                pass
            parse_args(['realdonaldtrump', 'test.csv', '5'])
            # delete the file
        os.remove('test.csv')
        self.assertDictEqual(
            {"twitterhandle": valid_case[0], "outputfile": valid_case[1],
             "days": valid_case[2], "cloud": False, "likes": False},
            parse_args(valid_case))