import re


def coupon_rows_to_wager_request(rows: str, draw_id: str, stake: str):
    def selections_to_sport_wager_request_obj(selections_):
        return {
            "type": "NORMAL",
            "drawId": draw_id,
            "gameName": "SPORT",
            "selections": selections_,
            "stake": stake
        }

    def out_comes_to_selections(oc):
        return [
            {'systemBetType': 'SYSTEM', 'outcomes': oc}
        ]

    def clean_up_row_string(r):
        return re.sub(r"[^1xX2]", '', r)

    def row_to_outcomes(r):
        return list(map(char_to_selection, r))

    def char_to_selection(c):
        char_to_selection_map = {
            '1': 'home',
            'x': 'tie',
            '2': 'away'
        }
        return {
            char_to_selection_map[c]: {
                "selected": True
            }
        }

    split_rows = re.split(r'[\r\n]', rows)
    not_empties = filter(lambda item: item, split_rows)
    cleaned_up_rows = map(clean_up_row_string, not_empties)
    outcomes = map(row_to_outcomes, cleaned_up_rows)
    selections = list(map(out_comes_to_selections, outcomes))
    request_objs = map(selections_to_sport_wager_request_obj, selections)
    return list(request_objs)
