from pprint import pprint
from typing import Mapping

import requests

# the veikkaus site address
host = "https://www.veikkaus.fi"

# required headers
headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
    'X-ESA-API-Key': 'ROBOT'
}


class ConnectionException(Exception):
    def __init__(self, msg, status_code):
        self.msg = msg
        self.status_code = status_code


def login(username, password):
    s = requests.Session()
    login_req = {"type": "STANDARD_LOGIN", "login": username, "password": password}
    try:
        r = s.post(host + "/api/bff/v1/sessions", verify=True, json=login_req, headers=headers)
        if r.status_code == 200:
            print(f'Login successful, {username} logged in')
            return s
        else:
            raise ConnectionException("Authentication failed", r.status_code)
    except Exception as e:
        raise ConnectionException("Connection failed", e)


def refresh_games(session):
    json = session.get("https://www.veikkaus.fi/api/sport-open-games/v1/games/SPORT/draws", headers=headers).json()
    pprint(json)
    return json


def send_games(session, coupons: Mapping):
    print(f'Sending: {len(coupons["boards"])} boards')
    r = session.post("https://www.veikkaus.fi/api/sport-interactive-wager/v1/tickets", headers=headers,
                     json=coupons)
    if r.status_code == 200:
        print(f'Success: {r}')
    else:
        print(f'Failed sending: {coupons}')
        raise ConnectionException(f'Sending coupons failed {r.status_code} {r.json()}', r.status_code)
    return r
