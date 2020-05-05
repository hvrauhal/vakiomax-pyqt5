import json
import os
import unittest
from datetime import datetime
from pathlib import Path

from vakiomax_pyqt5.parselines import coupon_rows_to_wager_requests, draws_to_options, GameOption


class TestParseLines(unittest.TestCase):
    def test_one(self):
        self.assertEqual([{'drawId': 'the_drawId',
                           'gameName': 'SPORT',
                           'selections': [{'outcomes': [{'home': {'selected': True}},
                                                        {'tie': {'selected': True}},
                                                        {'away': {'selected': True}}],
                                           'systemBetType': 'SYSTEM'}],
                           'stake': 'the_stake',
                           'type': 'NORMAL'}], coupon_rows_to_wager_requests('1x2', 'the_drawId', 'the_stake'))

    def test_extra_stuff(self):
        self.assertEqual([{'drawId': 'the_drawId',
                           'gameName': 'SPORT',
                           'selections': [{'outcomes': [{'home': {'selected': True}},
                                                        {'tie': {'selected': True}},
                                                        {'away': {'selected': True}}],
                                           'systemBetType': 'SYSTEM'}],
                           'stake': 'the_stake',
                           'type': 'NORMAL'}],
                         coupon_rows_to_wager_requests('   1bbbxfff2\n\n', 'the_drawId', 'the_stake'))

    def test_rows(self):
        self.assertEqual([{'drawId': 'the_drawId',
                           'gameName': 'SPORT',
                           'selections': [{'outcomes': [{'home': {'selected': True}}],
                                           'systemBetType': 'SYSTEM'}],
                           'stake': 'the_stake',
                           'type': 'NORMAL'},
                          {'drawId': 'the_drawId',
                           'gameName': 'SPORT',
                           'selections': [{'outcomes': [{'tie': {'selected': True}}],
                                           'systemBetType': 'SYSTEM'}],
                           'stake': 'the_stake',
                           'type': 'NORMAL'},
                          {'drawId': 'the_drawId',
                           'gameName': 'SPORT',
                           'selections': [{'outcomes': [{'away': {'selected': True}}],
                                           'systemBetType': 'SYSTEM'}],
                           'stake': 'the_stake',
                           'type': 'NORMAL'}], coupon_rows_to_wager_requests('1\nx\n2', 'the_drawId', 'the_stake'))


class TestApiParsing(unittest.TestCase):
    def test_sample_draw(self):
        draws_sample = json.loads((Path(os.path.dirname(__file__)) / 'sample_draws.json').read_text('utf-8'))
        self.assertEqual(
            [GameOption(id='53961', base_price=10, name='Kaviovakio', close_time=datetime(2020, 5, 4, 20, 50)),
             GameOption(id='53963', base_price=10, name='Counter-strike-vakio',
                        close_time=datetime(2020, 5, 5, 15, 58)),
             GameOption(id='53962', base_price=10, name='Futisvakio', close_time=datetime(2020, 5, 8, 16, 58))],
            draws_to_options(draws_sample))
