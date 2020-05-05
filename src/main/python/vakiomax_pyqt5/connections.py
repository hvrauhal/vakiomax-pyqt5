import json

import requests

# the veikkaus site address
host = "https://www.veikkaus.fi"

# required headers
headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
    'X-ESA-APi-Key': 'ROBOT'
}


class LoginException(Exception):
    def __init__(self, msg, status_code):
        self.msg = msg
        self.status_code = status_code


def login(username, password):
    s = requests.Session()
    login_req = {"type": "STANDARD_LOGIN", "login": username, "password": password}
    r = s.post(host + "/api/bff/v1/sessions", verify=True, data=json.dumps(login_req), headers=headers)
    if r.status_code == 200:
        print(f'Login successful, {username} logged in')
        return s
    else:
        raise LoginException("Authentication failed", r.status_code)


def refresh_games(session):
    return session.get("https://www.veikkaus.fi/api/v1/sport-games/draws?game-names=SPORT", headers=headers).json()

