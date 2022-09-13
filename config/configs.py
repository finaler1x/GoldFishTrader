import json
from typing import List

from prodict import Prodict


# secrets.json
class Sandbox(Prodict):
    api_key: str
    api_secret: str


class Alpaca(Prodict):
    sandbox: Sandbox


class Reddit(Prodict):
    client_id: str
    api_key: str
    client_secret: str
    username: str
    password: str


class Secret(Prodict):
    reddit: Reddit
    alpaca: Alpaca


# constants.json
class Modifier(Prodict):
    gain_flair: str


class Urls(Prodict):
    constRedditWallstreetbetsUrl: str


class Constants(Prodict):
    urls: Urls
    modifier: Modifier


# handle configs

with open('config/secrets.json') as file:
    data = json.load(file)
    secret: Secret = Secret.from_dict(data)

with open('config/constants.json') as file:
    data = json.load(file)
    constant: Constants = Constants.from_dict(data)
