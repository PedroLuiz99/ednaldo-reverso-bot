# -*- coding: utf-8 -*-

import os
from logger import Logger
import argparse
import configparser


parser = argparse.ArgumentParser(description="A Twitter bot to revert tweets and reply to @oednaldopereira")
parser.add_argument("-c", "--config", action="store", required=False, dest="config_file",
                    default="./ednaldo_reverso.ini",
                    help="Specify custom configuration file. The default is './ednaldo_reverso.ini'.")

parser.add_argument("-d", "--debug", required=False, action="store_true", dest="debug", default=False,
                    help="Enable debug messages.")
args = parser.parse_args()

DEBUG = args.debug
CONFIG_FILE = args.config_file

if os.path.isfile(CONFIG_FILE):
    Logger.file_write = True

Logger.info("Teste")

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
print(config)


