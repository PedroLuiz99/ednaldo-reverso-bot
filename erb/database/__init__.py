# -*- coding: utf-8 -*-

import sys
import sqlite3
from erb.config import config
from erb.logger import Logger

from datetime import datetime, timezone

dbf = config['database']['sqlite_file']


def create_database():
    try:
        conn = sqlite3.connect(dbf)
        cursor = conn.cursor()

        cursor.execute("""
    CREATE TABLE tweets (
        id INTEGER NOT NULL PRIMARY KEY,
        answered INTEGER NOT NULL,
        answered_on DATE
    );
    """)
    except sqlite3.OperationalError as e:
        Logger.error("Error initializing database: {}".format(str(e)))
        sys.exit(6)
    finally:
        conn.close()


def save_replied_tweet(tweet_id, code):
    conn = sqlite3.connect(dbf)
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO tweets VALUES (?, ?, ?)""", (tweet_id, code, datetime.now(timezone.utc)))
    conn.commit()
    conn.close()

    # TODO: Raise sqlite3.IntegrityError

