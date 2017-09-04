import random
from exceptions import UpdateError

from setup import TWITTER_API_ID, EXCHANGE_RATE_API_ID

INTERVAL = 3600
LAST_UPDATE_TIME = INTERVAL * 11  # 12 updates, first one is at t=0


def get_next_update(apis, last_updated_time=None):
    if (last_updated_time is None or last_updated_time == LAST_UPDATE_TIME):
        next_update_time = 0
    else:
        next_update_time = last_updated_time + INTERVAL

    update = SCHEDULE[next_update_time]
    configuration = {**apis, 'update_time': next_update_time}

    return update(configuration)


class Update:
    def __init__(self, config):
        self.config = config

    @property
    def time(self):
        return self.config['update_time']


class WorldWideTrendUpdate(Update):
    WORLD_WOEID = 1
    TEMPLATES = [
        "{tweet_volume} people worldwide a tweet bout dis enuh: {name}, pre: {url}",
        "{tweet_volume} people worldwide a tweet bout {name}, see wah gwan {url}",
        "Hol' on... {tweet_volume} people worldwide still a chat bout {name}? pre: {url}",
        "{tweet_volume} people round d world a tweet bout {name}, unuh look yah {url}"]

    def __init(self, apis):
        Update.__init__(config)

    def format(self, trend):
        # tweet_volume is either None or a number
        if trend['tweet_volume'] is None:
            trend['tweet_volume'] = random.choice(
                ['nuff', "hol' heap a", 'a bagga'])
        # Remove the hash tag (if any) from the name because of Twitter policy
        if trend['name'][0] == '#':
            trend['name'] = trend['name'][1:]
        template = random.choice(self.TEMPLATES)
        return template.format(**trend)

    def update(self):
        try:
            twitter_api = self.config[TWITTER_API_ID]
            worldwide_trends = twitter_api.trends_place(self.WORLD_WOEID)[0]

            # Only tweet Ascii trends
            valid_trend = False
            while not valid_trend:
                random_trend = random.choice(worldwide_trends['trends'])
                try:
                    random_trend['name'].encode('ascii')
                    valid_trend = True
                except UnicodeEncodeError:
                    pass

            tweet = self.format(random_trend)
            twitter_api.update_status(tweet)

        except Exception as e:
            raise UpdateError(e)


class ExchangeRateUpdate(Update):
    TEMPLATES = [
        "Mek we see how the dollar doing nuh.. {jmd_usd:.2f} JMD to 1 USD, {jmd_gbp:.2f} JMD fi 1 GBP and {jmd_eur:.2f} JMD to 1 EUR",
        "Currency watch, unuh look yah: {jmd_usd:.2f} JMD to 1 USD, {jmd_gbp:.2f} JMD to 1 GBP and {jmd_eur:.2f} JMD to 1 EUR",
        "Since me last look: whola {jmd_usd:.2f} JMD fi 1 USD, {jmd_gbp:.2f} JMD to 1 GBP and {jmd_eur:.2f} JMD to 1 EUR"]

    def __init__(self, config):
        Update.__init__(self, config)

    def format(self, rates):
        template = random.choice(self.TEMPLATES)
        return template.format(**rates)

    def update(self):
        try:
            exchange_rate_api = self.config[EXCHANGE_RATE_API_ID]
            twitter_api = self.config[TWITTER_API_ID]

            latest_rates = exchange_rate_api.latest()
            jmd = latest_rates['JMD']
            gbp = latest_rates['GBP']
            euro = latest_rates['EUR']

            rate_dict = {
                'jmd_usd': jmd,
                'jmd_gbp': jmd / gbp,
                'jmd_eur': jmd / euro,
            }

            tweet = self.format(rate_dict)
            twitter_api.update_status(tweet)
        except Exception as e:
            raise UpdateException(e)


class JamaicanEventUpdate(Update):
    TEMPLATES = ["Mad party name {title} a gwaan on {date}.{summary}",
                 "You need fi touch {title}.Duh road pon {date}.{summary}"
                 ]

    def __init__(self, config):
        Update.__init__(self, config)

    def format(self, event):
        template = random.choice(self.TEMPLATES)
        return template.format(**event)

    def update(self):
        try:

            twitter_api = self.config[TWITTER_API_ID]
            web_scrapper = WebScraper()
            events = web_scrapper.parse_events("http://pripsjamaica.com/events/list/8/parties")
            latest_event = events[0]

            event_dict = {
                'title': event.title,
                'date': event.date,
                'summary': event.summary,
            }

            tweet = self.format(event_dict)
            twitter_api.update_status(tweet)
        except Exception as e:
            raise UpdateException(e)

class RetweetUpdate(Update):
    def update(self):
        try:
            twitter_api = self.config[TWITTER_API_ID]
            worldwide_trends = twitter_api.trends_place(self.WORLD_WOEID)[0]

            # Only tweet Ascii trends
            valid_trend = False
            while not valid_trend:
                random_trend = random.choice(worldwide_trends['trends'])
                try:
                    random_trend['name'].encode('ascii')
                    trend = random_trend['name']
                    for tweet in tweepy.Cursor(api.search,q=trend,since='2016-11-25',
                           until='2016-11-27',
                           geocode='18.02323,-77.2323,100km',
                           lang='eng').items(10):
                        try:
                            tweet.retweet()
                        except tweepy.TweepError as e:
                            print(e.reason)
                        except StopIteration:
                            break

                    
                    valid_trend = True
                except UnicodeEncodeError:
                    pass

        except Exception as e:
            raise UpdateException(e)

    


SCHEDULE = {
    0: WorldWideTrendUpdate,
    INTERVAL * 1: WorldWideTrendUpdate,
    INTERVAL * 2: ExchangeRateUpdate,
    INTERVAL * 3: WorldWideTrendUpdate,
    INTERVAL * 4: WorldWideTrendUpdate,
    INTERVAL * 5: WorldWideTrendUpdate,
    INTERVAL * 6: WorldWideTrendUpdate,
    INTERVAL * 7: WorldWideTrendUpdate,
    INTERVAL * 8: WorldWideTrendUpdate,
    INTERVAL * 9: WorldWideTrendUpdate,
    INTERVAL * 10: WorldWideTrendUpdate,
    LAST_UPDATE_TIME: WorldWideTrendUpdate
}
