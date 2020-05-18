from datetime import datetime
import logging as log
import os

def red(text): return '\033[0;31m' + text + '\033[0m'
def green(text): return '\033[0;32m' + text + '\033[0m'
def yellow(text): return '\033[0;33m' + text + '\033[0m'
def blue(text): return '\033[0;34m' + text + '\033[0m'
def magenta(text): return '\033[0;35m' + text + '\033[0m'
def cyan(text): return '\033[0;36m' + text + '\033[0m'
def white(text): return '\033[0;37m' + text + '\033[0m'


class Console:
    """
    0: emergency
    1: alert
    2: critical
    3: error
    4: warning
    5: notice
    6: info
    7: debug
    """

    def __init__(self, level=6):
        self.level = level
        log.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))        

    def get_datetime(self):
            now = datetime.now()
            return now.strftime("%d/%m/%Y %H:%M:%S")

    def emergency(self, message):
        if self.level >= 0:
            dt = self.get_datetime()
            data = dt + magenta(' EMERGENCY: ') + message
            print(data)

    def alert(self, message):
        if self.level >= 1:
            dt = self.get_datetime()
            data = dt + magenta(' ALERT: ') + message
            print(data)

    def critical(self, message):
        if self.level >= 2:
            dt = self.get_datetime()
            data = dt + magenta(' CRITICAL: ') + message
            print(data)

    def error(self, message):
        if self.level >= 3:
            dt = self.get_datetime()
            data = dt + red(' ERROR: ') + message
            print(data)

    def warning(self, message):
        if self.level >= 4:
            dt = self.get_datetime()
            data = dt + yellow(' WARNING: ') + message
            print(data)

    def notice(self, message):
        if self.level >= 5:
            dt = self.get_datetime()
            data = dt + blue(' NOTICE: ') + message
            print(data)

    def info(self, message):
        if self.level >= 6:
            dt = self.get_datetime()
            data = dt + green(' INFO: ') + message
            print(data)

    def debug(self, message):
        if self.level >= 7:
            dt = self.get_datetime()
            data = dt + white(' DEBUG: ') + message
            print(data)
