# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import uuid
import pathlib
import twitter
import requests

from erb import database
from erb.reverter import revert_video, revert_photo
from erb.config import config
from erb.logger import Logger

TWITTER_USER = None


def download_media(url, fmt):
    # TODO: REMOVER SELETOR DE FORMATO
    try:
        pathlib.Path(config['paths']['download_path']).mkdir(exist_ok=True)
    except OSError as e:
        Logger.error("Error creating download folder!")
        Logger.debug(e)
        sys.exit(7)

    try:
        internal_media_id = uuid.uuid4()
        video_path = os.path.join(config['paths']['download_path'], "{}.{}".format(internal_media_id, fmt))
        video = requests.get(url, allow_redirects=True)
        open(video_path, 'wb').write(video.content)
        return {
            'file': video_path,
            'internal_media_id': internal_media_id
        }
    except Exception as e:
        raise


def fetch_replies(api):
    store_count = 0
    since = 0
    while True:
        replies = api.GetReplies(since_id=since)
        for reply in replies:
            if hasattr(reply, 'in_reply_to_screen_name') and \
                    reply.in_reply_to_screen_name == config['twitter']['seek_user']:
                assert database.store_tweet(reply.id, 1)
                Logger.debug("\tStored tweet ID {}".format(reply.id))
                since = reply.id if reply.id > since else since
                store_count += 1

        if len(replies) < 20:
            break
    Logger.info("\tStored {} replied tweets to database.".format(store_count))


def process_media(tweet):
    processed_media = []
    for media in tweet.media:
        if media.type == 'video':
            url = ''
            for v in media.video_info['variants']:
                if v['content_type'] == 'video/mp4':
                    url = v['url']
                    Logger.info("Video found, downloading...")
                    Logger.debug("\tVideo URL: {}".format(url))
                    break

            if url:
                try:
                    downloaded = download_media(url, 'mp4')
                    processed_media.append({'type': 'video', 'path': revert_video(**downloaded)})
                except Exception as e:
                    Logger.error("Error downloading media!")
                    Logger.debug("\tException: {}".format(str(e)))

        elif media.type == 'photo':
            Logger.info("\tPhoto found, downloading...")
            downloaded = download_media(media.media_url_https, 'png')
            processed_media.append({'type': 'photo', 'path': revert_photo(**downloaded)})

    return processed_media


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
    while True:
        Logger.info("Feching last replied tweet")
        last_replied = database.get_last_replied_tweet()

        if last_replied is None:
            Logger.info("No tweets found, processing timeline and getting last 20 tweets.")
            fetch_replies(api)
            get_since = None
        else:
            get_since = last_replied

        statuses = api.GetUserTimeline(TWITTER_USER.id, since_id=get_since)

        for status in statuses:
            Logger.info("Processing tweet {}".format(status.id))

            text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '',
                          status.text)[::-1]
            Logger.debug("Tweet text: {}".format(text))
            Logger.info("\tProcessing media...")
            processed_media = []
            if status.media is not None:
                processed_media = process_media(status)

            Logger.info("Uploading media...")
            uploaded_media = []
            for media in processed_media:
                if media['type'] == 'video':
                    media_ = api.UploadMediaChunked(media=media['path'], media_category='tweet_video')
                    Logger.info("Video uploaded, waiting server-side processing to continue...")
                    time.sleep(10)
                else:
                    media_ = api.UploadMediaSimple(media=media['path'], media_category='tweet_video')
                    Logger.info("Video uploaded, waiting server-side processing to continue...")
                    time.sleep(10)
                uploaded_media.append(media_)
            posted = api.PostUpdate(status=text, media=uploaded_media, in_reply_to_status_id=status.id)
            Logger.debug(str(posted))
            database.store_tweet(posted.id, 1)

        Logger.info("Finished! Waiting next execution...")
        time.sleep(60)

