# -*- coding: utf-8 -*-

import config
import inspect

from datetime import datetime
from enum import Enum
from sys import stdout


class Logger:
    file_write = False

    class LogLevel(Enum):
        INFO = 10
        WARNING = 20
        ERROR = 30
        DEBUG = 40

    breaks = {
        True: "\n",
        False: ""
    }

    @staticmethod
    def write_log(message, break_line=True, level=LogLevel.INFO):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)

        formatted_message = "[{date}] [{level}] [{frame}] {message} {break_line}".format(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            level=level.name.lower(),
            frame=calframe[2][3],
            message=message,
            break_line=Logger.breaks[break_line]
        )

        stdout.write(formatted_message)
        stdout.flush()

    @staticmethod
    def info(message, break_line=True):
        Logger.write_log(message, break_line, Logger.LogLevel.INFO)

    @staticmethod
    def warning(message, break_line=True):
        Logger.write_log(message, break_line, Logger.LogLevel.WARNING)

    @staticmethod
    def error(message, break_line=True):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        Logger.write_log(message, break_line, Logger.LogLevel.ERROR)

    @staticmethod
    def debug(message, break_line=True):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        Logger.write_log(message, break_line, Logger.LogLevel.DEBUG)
