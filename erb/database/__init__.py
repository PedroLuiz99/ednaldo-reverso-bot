# -*- coding: utf-8 -*-

import sys
import sqlite3
from erb.config import config
from erb.logger import Logger

from datetime import datetime, timezone

dbf = config['database']['sqlite_file']


def query(sql, params=None, return_dataset=True):
    if params is None:
        params = []

    try:
        with sqlite3.connect(dbf) as conn:
            cursor = conn.cursor()
            result = cursor.execute(sql, params)
            if return_dataset:
                return result.fetchall()
            return result.rowcount()
    except Exception as e:
        Logger.debug("Error executing statement: \nStatement: {}\nParameters: {}\nException: {}".format(
            sql,
            str(params),
            str(e))
        )
        raise e


def execute(sql, params):
    return query(sql, params, return_dataset=False)


def create_database():
    try:
        execute("""
        CREATE TABLE tweets (
            id INTEGER NOT NULL PRIMARY KEY,
            replied INTEGER NOT NULL,
            replied_on DATE,
            reply_link VARCHAR 
        );
        """)
    except Exception as e:
        Logger.error("Error initializing database!")
        sys.exit(6)


def store_tweet(tweet_id, code, link):
    try:
        res = execute("""INSERT INTO tweets VALUES (?, ?, ?, ?)""", (tweet_id, code, datetime.now(timezone.utc), link), )
        return bool(res)
    except Exception as e:
        return False


def get_last_replied_tweet():
    try:
        return query("SELECT * FROM tweets WHERE replied = 1 ORDER BY replied_on DESC LIMIT 1")
    except Exception as e:
        Logger.error("Cannot fetch tweet history!")
        raise


def get_all_tweets():
    try:
        return query("SELECT * FROM tweets")
    except Exception as e:
        Logger.error("Cannot get stored tweets")
        raise
