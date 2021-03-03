import json
import os
import unittest
from datetime import datetime
from pathlib import Path

from vakiomax_pyqt5.parselines import coupon_rows_to_wager_requests, draws_to_options, GameOption


class TestParseLines(unittest.TestCase):
    def test_one(self):
        self.assertEqual({'boards': [{'betType': 'Regular',
                                      'selections': [{'outcomes': ['1']},
                                                     {'outcomes': ['X']},
                                                     {'outcomes': ['2']}],
                                      'stake': 123}],
                          'gameName': 'SPORT',
                          'listIndex': 2}, coupon_rows_to_wager_requests('1x2', 2, 123))

    def test_extra_stuff(self):
        self.assertEqual({'boards': [{'betType': 'Regular',
                                      'selections': [{'outcomes': ['1']},
                                                     {'outcomes': ['X']},
                                                     {'outcomes': ['2']}],
                                      'stake': 123}],
                          'gameName': 'SPORT',
                          'listIndex': 2},
                         coupon_rows_to_wager_requests('   1bbbxfff2\n\n', 2, 123))

    def test_rows(self):
        self.assertEqual({'boards': [{'betType': 'Regular',
                                      'selections': [{'outcomes': ['1']}],
                                      'stake': 123},
                                     {'betType': 'Regular',
                                      'selections': [{'outcomes': ['X']}],
                                      'stake': 123},
                                     {'betType': 'Regular',
                                      'selections': [{'outcomes': ['2']}],
                                      'stake': 123}],
                          'gameName': 'SPORT',
                          'listIndex': 2}, coupon_rows_to_wager_requests('1\nx\n2', 2, 123))


class TestApiParsing(unittest.TestCase):
    def test_sample_draw(self):
        draws_sample = json.loads((Path(os.path.dirname(__file__)) / 'sample_open_games.json').read_text('utf-8'))
        self.assertEqual(
            [GameOption(list_index='1',
                        base_price=25,
                        name='Vakio',
                        close_time=datetime(2020, 10, 17, 16, 58),
                        rows_count=13),
             GameOption(list_index='5',
                        base_price=10,
                        name='Futisvakio',
                        close_time=datetime(2020, 10, 14, 18, 58),
                        rows_count=14),
             GameOption(list_index='6',
                        base_price=10,
                        name='Futisvakio',
                        close_time=datetime(2020, 10, 15, 17, 58),
                        rows_count=11),
             GameOption(list_index='9',
                        base_price=10,
                        name='Counter-Strike-vakio',
                        close_time=datetime(2020, 10, 15, 13, 58),
                        rows_count=8)],
            draws_to_options(draws_sample))
