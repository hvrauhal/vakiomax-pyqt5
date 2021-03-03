import re
from collections import Mapping
from dataclasses import dataclass
from datetime import datetime


def coupon_rows_to_wager_requests(rows: str, list_index: str, stake: int):
    def clean_up_row_string(r):
        return re.sub(r"[^1X2]", '', r)

    def row_to_board(r):
        return {'betType': 'Regular', 'stake': stake, 'selections': list(map(char_to_outcomes, r))}

    def char_to_outcomes(c):
        return {
            'outcomes': [c]
        }

    upper_rows = rows.upper()
    split_rows = re.split(r'[\r\n]', upper_rows)
    not_empties = filter(lambda item: item, split_rows)
    cleaned_up_rows = map(clean_up_row_string, not_empties)
    boards = list(map(row_to_board, cleaned_up_rows))
    return {
        "listIndex": list_index,
        "gameName": "SPORT",
        "boards": boards,
        "price": sum([board['stake'] for board in boards])
    }


@dataclass(frozen=True)
class GameOption:
    list_index: str
    base_price: int
    name: str
    close_time: datetime
    rows_count: int


def draws_to_options(draws: Mapping):
    open_draws = (d for d in draws if d['status'] == 'OPEN')
    return [
        GameOption(list_index=i['listIndex'],
                   base_price=i['gameRuleSet']['basePrice'],
                   name=i['name'],
                   close_time=datetime.fromtimestamp(i['closeTime'] / 1000.0),
                   rows_count=len(i['rows']))
        for i in open_draws]
