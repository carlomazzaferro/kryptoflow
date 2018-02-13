import pkg_resources
import os
import sys
import configparser
import json
from kryptoflow.definitions import CONFIG_PATH
from datetime import datetime, time


def load_conf():
    with open(CONFIG_PATH, 'r') as inf:
        return json.load(inf)


class Timer(object):
    def __init__(self):
        self._last_timestamp = datetime.now().timestamp()

    @property
    def last_timestamp(self):
        return self._last_timestamp

    @last_timestamp.setter
    def last_timestamp(self, timestamp):
        self._last_timestamp = timestamp

    @property
    def now(self):
        return datetime.now().timestamp()

    def elapsed_time(self, other):
        return self.now - other

    @property
    def closest_fith(self):
        return int(5 * round(float(self.now)/5))