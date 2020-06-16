# -*- coding: utf-8 -*-

from erb import bot, config, database

if __name__ == '__main__':
    if config.config.getboolean('runtime', 'createdb'):
        database.create_database()

    bot.start()
