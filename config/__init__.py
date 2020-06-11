# -*- coding: utf-8 -*-

import logger
import argparse
import configparser
from sys import stdout, exit

parser = argparse.ArgumentParser(description="A Twitter bot to revert tweets and reply to @oednaldopereira")
parser.add_argument("-c", "--config", action="store", required=False, dest="config_file",
                    default="./ednaldo_reverso.ini",
                    help="Specify custom configuration file. The default is './ednaldo_reverso.ini'.")

parser.add_argument("-d", "--debug", required=False, action="store_true", dest="debug", default=False,
                    help="Enable debug messages.")
args = parser.parse_args()


config = configparser.ConfigParser()
try:
    if not config.read(args.config_file):
        if args.config_file == './ednaldo_reverso.ini':
            config['logging'] = {
                'log_file': 'ednaldo.log',
                'log_level': 'info',
            }

            config['twitter'] = {
                'secret': '',
                'key': ''
            }

            with open(args.config_file, 'w') as dcf:
                config.write(dcf)

        else:
            logger.emergency_log("Cannot open config file, check parameters. Exiting...", 1)
except Exception as e:
    logger.emergency_log(str(e), 2)


logger.init_logger(
    log_level=logger.LogLevel.DEBUG if args.debug else logger.LogLevel.INFO,
    log_file=config['logging']['log_file']
)

logger.Logger.info("Teste")
logger.Logger.warning("Teste2")
logger.Logger.error("Teste3")
