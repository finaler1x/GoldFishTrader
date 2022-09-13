import requests
import re
import csv

from config import configs


def init_reddit_connection():
    reddit_secrets = configs.secret.reddit

    auth = requests.auth.HTTPBasicAuth(
        reddit_secrets.client_id,
        reddit_secrets.bot_secret
    )

    data = {
        'grant_type': 'password',
        'username': reddit_secrets.username,
        'password': reddit_secrets.password
    }

    headers = {'User-Agent': 'MyBot/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    token = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {token}"}}

    try:
        res = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('Bad Status Code from Reddit Auth', err)
        raise err

    return headers


def get_wallstreetbets_posts(headers, modifier):
    url = configs.constant.urls.redditWallstreetbetsUrl

    try:
        res = requests.get(url + modifier, headers=headers)
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('Bad Status Code', err)
        raise err

    return res.json()['data']['children']


def choose_ticker(posts):
    best_post = {}
    best_ticker = ""

    for post in posts:
        # check for gain flair
        if post['data']['link_flair_richtext'][0]['t'] == configs.constant.modifier.gain_flair:
            ticker_symbol = ticker_symbol_check(post)

            # check if post contains trade relevant data
            if ticker_symbol:
                post_score = post['data']["ups"] - post['data']["downs"]

                # compare post value
                if best_post:
                    best_post_score = best_post['data']["ups"] - best_post['data']["downs"]
                else:
                    best_post_score = 0

                if post_score > best_post_score:
                    best_post = post
                    best_ticker = ticker_symbol

    return best_ticker


def ticker_symbol_check(post):
    title = post['data']['title']
    pattern = '([A-Z^][A-Z^]+)'
    result = re.findall(pattern, title)

    if result:
        with open(configs.constant.paths.ticker_symbol_path, 'r') as csvfile:
            my_content = csv.reader(csvfile, delimiter=';')
            for row in my_content:
                if result[0] in row:
                    return result[0]

    return result


def prepare_reddit_trade():
    headers = init_reddit_connection()
    posts = get_wallstreetbets_posts(headers, configs.constant.modifier.today_top)
    ticker = choose_ticker(posts)

    return ticker
