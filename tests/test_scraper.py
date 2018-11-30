import unittest

from ..src.tweets2csv.scraper import validate_twitter

class TestTwitterScraper(unittest.TestCase):
    def test_case(self):
        validate_twitter()