# -*- coding: utf-8 -*-

from erb import logger

import os
import argparse
import configparser
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
default_config = os.path.join(project_root, 'ednaldo_reverso.ini')
default_log_file = os.path.join(project_root, 'ednaldo.log')
default_database_file = os.path.join(project_root, 'ednaldo.db')
default_download_path = os.path.join(project_root, 'downloads')

parser = argparse.ArgumentParser(description="A Twitter bot to revert tweets and reply to @oednaldopereira")
parser.add_argument("-c", "--config", action="store", required=False, dest="config_file",
                    default=default_config,
                    help="Specify custom configuration file. The default is '<project_root>/ednaldo_reverso.ini'.")

parser.add_argument("-d", "--debug", required=False, action="store_true", dest="debug", default=False,
                    help="Enable debug messages.")

parser.add_argument('--start', action='store_true', dest='start_bot', help="Starts the bot", default=False)
parser.add_argument('--createdb', action='store_true', dest='cdb', help="Create the tweet database", default=False)
args = parser.parse_args()

config = configparser.ConfigParser()
try:
    if not config.read(args.config_file):
        if args.config_file == default_config:
            config['logging'] = {
                'log_file': 'default',
                'log_level': 'info',
            }

            config['twitter'] = {
                'consumer_key': '',
                'consumer_secret': '',
                'access_token': '',
                'access_secret': '',
                'seek_user': 'oednaldopereira',
                'origin_user': 'arierepodlandeo'
            }

            config['database'] = {
                'sqlite_file': 'default'
            }

            config['paths'] = {
                'download_path': 'default'
            }

            with open(args.config_file, 'w') as dcf:
                config.write(dcf)
            logger.emergency_log("Please fill the parameters in config file...", 3)
        else:
            logger.emergency_log("Cannot open config file, check parameters. Exiting...", 1)
except Exception as e:
    logger.emergency_log(str(e), 2)

if config['logging']['log_file'] == 'default':
    config['logging']['log_file'] = default_log_file

if config['database']['sqlite_file'] == 'default':
    config['database']['sqlite_file'] = default_database_file

if config['paths']['download_path'] == 'default':
    config['paths']['download_path'] = default_download_path

config['runtime'] = {
    'createdb': args.cdb,
    'start': args.start_bot
}
logger.init_logger(
    log_level=logger.LogLevel.DEBUG if args.debug or config['logging']['log_level'] == 'debug'
    else logger.LogLevel.INFO,
    log_file=config['logging']['log_file']
)
