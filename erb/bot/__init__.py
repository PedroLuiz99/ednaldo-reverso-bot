# -*- coding: utf-8 -*-

import os
import re
import sys
import uuid
import pathlib
import twitter
import requests

from erb import database
from erb.reverter import revert_video
from erb.config import config
from erb.logger import Logger

TWITTER_USER = None


def download_media(url):
    try:
        pathlib.Path(config['paths']['download_path']).mkdir(exist_ok=True)
    except OSError as e:
        Logger.error("Error creating download folder!")
        Logger.debug(e)
        sys.exit(7)

    try:
        internal_media_id = uuid.uuid4()
        video_path = os.path.join(config['paths']['download_path'], "{}.mp4".format(internal_media_id))
        video = requests.get(url, allow_redirects=True)
        open(video_path, 'wb').write(video.content)
        return {
            'file': video_path,
            'internal_media_id': internal_media_id
        }
    except Exception as e:
        raise


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

    Logger.info("Feching last replied tweet")
    last_replied = database.get_last_replied_tweet()

    if not last_replied:
        Logger.info("No tweets found, getting last 20 tweets.")
        get_since = None
    else:
        get_since = last_replied[0]

    statuses = api.GetUserTimeline(TWITTER_USER.id, since_id=get_since)

    for status in statuses:
        Logger.info("Processing tweet {}".format(status.id))
        text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '',
                      status.text)[::-1]
        Logger.info("\tProcessing media...")
        for media in status.media:
            if media.type == 'video':
                url = ''
                for v in media.video_info['variants']:
                    if v['content_type'] == 'video/mp4':
                        url = v['url']
                        Logger.info("\tVideo found...")
                        Logger.debug("\t\tVideo URL: {}".format(url))
                        break

                if url:
                    try:
                        downloaded = download_media(url)
                        revert_video(**downloaded)
                    except Exception as e:
                        Logger.error("\tError downloading media!")
                        Logger.debug("\t\tException: {}".format(str(e)))

            elif media.type == 'image':
                pass
                # TODO: PROCESSAR  IMAGEM
