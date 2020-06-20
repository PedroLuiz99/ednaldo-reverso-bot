# -*- coding: utf-8 -*-

from sys import stdout
from pyfiglet import Figlet

from erb import bot, config, database

if __name__ == '__main__':

    figlet = Figlet(font='colossal', width=200)
    stdout.write(figlet.renderText("EdnaldoReversoBOT"))
    if config.config.getboolean('runtime', 'createdb'):
        database.create_database()

    bot.start()
