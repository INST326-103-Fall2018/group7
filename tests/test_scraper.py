import unittest

from GroupProject.tweets2csv.src.scraper import validate_twitter

class TestTwitterScraper(unittest.TestCase):
    def test_case(self):
        validate_twitter()