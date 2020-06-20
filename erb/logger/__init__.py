# -*- coding: utf-8 -*-

from . import caller

from datetime import datetime
from enum import Enum
from sys import stdout


class LogLevel(Enum):
    INFO = 10
    WARNING = 20
    ERROR = 30
    DEBUG = 40


colors = {
    'INFO': '\033[94m',
    'DEBUG': '\033[92m',
    'WARNING': '\033[93m',
    'ERROR': '\033[91m',
}

DISABLE_FILE_WRITE = False
LOG_LEVEL = LogLevel.INFO
LOG_FILE = None


def init_logger(log_level=LogLevel.INFO, log_file=None):
    global DISABLE_FILE_WRITE, LOG_LEVEL, LOG_FILE
    LOG_LEVEL = log_level
    LOG_FILE = log_file


def emergency_log(message, rc=0):
    stdout.write(message)
    stdout.flush()
    exit(rc)


class Logger:
    file_write = False

    breaks = {
        True: "\n",
        False: ""
    }

    @staticmethod
    def write_log(message, break_line=True, break_line_before=False, level=LogLevel.INFO, quiet=False):
        global DISABLE_FILE_WRITE
        _caller = caller.caller_name(2)

        level_stdout = "{level_color}[{level}]\033[0m".format(level=level.name.lower(), level_color=colors[level.name])
        level_file = "[{level}]".format(level=level.name.lower())

        formatted_message = "{blb}[{date}] #LEVEL# [{frame}] {message} {bla}".format(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            frame=_caller,
            message=str(message),
            bla=Logger.breaks[break_line],
            blb=Logger.breaks[break_line_before]
        )

        stdout.write(formatted_message.replace('#LEVEL#', level_stdout))
        stdout.flush()

        if DISABLE_FILE_WRITE:
            return
        try:
            try:
                with open(LOG_FILE, 'a') as lf:  # noqa
                    lf.write(formatted_message.replace('#LEVEL#', level_file))
            except FileNotFoundError:
                raise Exception("No such directory for logging, check config.")
            except PermissionError:
                raise Exception("Permission denied on logs folder.")
            except TypeError:
                raise Exception("Log directory configuration not provided.")
        except Exception as e:
            if not quiet:
                DISABLE_FILE_WRITE = True
                Logger.write_log(
                    "---> ERROR WRITING LOG TO FILE: '{}', LOG TO FILE WILL BE DISABLED FOR NOW.".format(str(e)),
                    break_line_before=True,
                    level=LogLevel.ERROR,
                    quiet=True)

    @staticmethod
    def info(message, break_line=True):
        Logger.write_log(message, break_line=break_line, level=LogLevel.INFO)

    @staticmethod
    def warning(message, break_line=True):
        Logger.write_log(message, break_line=break_line, level=LogLevel.WARNING)

    @staticmethod
    def error(message, break_line=True):
        Logger.write_log(message, break_line=break_line, level=LogLevel.ERROR)

    @staticmethod
    def debug(message, break_line=True):
        if LOG_LEVEL != LogLevel.DEBUG:
            return
        Logger.write_log(message, break_line=break_line, level=LogLevel.DEBUG)
