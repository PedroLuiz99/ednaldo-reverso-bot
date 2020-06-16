# -*- coding: utf-8 -*-

import sys
import twitter
from erb.config import config
from erb.logger import Logger
from erb import database

TWITTER_USER = None


def start():
    global TWITTER_USER
    try:
        api = twitter.Api(consumer_key=config['twitter']['consumer_key'],
                          consumer_secret=config['twitter']['consumer_secret'],
                          access_token_key=config['twitter']['access_token'],
                          access_token_secret=config['twitter']['access_secret'])

        TWITTER_USER = api.GetUser(screen_name=config['twitter']['seek_user'])
    except KeyError as e:
        Logger.error("Verify tokens in supplied config file...")
        sys.exit(4)
    except twitter.error.TwitterError as e:
        Logger.error("Error fetching user information: {}".format(str(e)))
        sys.exit(5)
    statuses = api.GetUserTimeline(TWITTER_USER.id)

    [database.save_replied_tweet(s.id, 1) for s in statuses]


