import tweepy
from oxr import OXR as OpenExchangeRatesClient

from credentials import *

TWITTER_API_ID = 'twitter'
EXCHANGE_RATE_API_ID = 'exchange'


def setup_apis():
    apis = {}

    apis[TWITTER_API_ID] = setup_twitter_api()
    apis[EXCHANGE_RATE_API_ID] = setup_exchange_rate_api()

    return apis


def setup_twitter_api():
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tweepy.API(auth)
    return api


def setup_exchange_rate_api():
    client = OpenExchangeRatesClient(
        app_id=open_exchange_rates_api_id, base='USD')
    return client
