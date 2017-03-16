import tweepy
import random
from time import sleep

# Import our Twitter credentails from credentials.py
from credentials import *

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

WORLD_WOEID = 1
INTERVAL = 3600
TEMPLATES = [
    "{tweet_volume} people worldwide a tweet bout dis enuh: {name}, pre: {url}",
    "{tweet_volume} people worldwide a tweet bout {name}, see wah gwan {url}",
    "Hol' on... {tweet_volume} people worldwide still a chat bout {name}? pre: {url}"
    "{tweet_volume} people round d world a tweet bout {name}, unuh look yah {url}"]


def format_tweet(trend):
    # Tweet_volume is either None or a number
    if trend['tweet_volume'] is None:
        trend['tweet_volume'] = random.choice(
            ['nuff', "hol' heap a", 'a bagga'])
    # Remove the hash tag (if any) because of Twitter policy
    if trend['name'][0] == '#':
        trend['name'] = trend['name'][1:]
    template = random.choice(TEMPLATES)
    return template.format(**trend)


while True:
    try:
        # Returns a list size 1 by default
        worldwide_trends = api.trends_place(WORLD_WOEID)[0]

        # Only tweet Ascii trends
        valid_tweet = False
        while not valid_tweet:
            random_trend = random.choice(worldwide_trends['trends'])
            try:
                random_trend['name'].encode('ascii')
                valid_tweet = True
            except UnicodeEncodeError:
                pass

        tweet = format_tweet(random_trend)
        api.update_status(tweet)

    except tweepy.TweepError as e:
        print(e.reason)

    sleep(INTERVAL)
