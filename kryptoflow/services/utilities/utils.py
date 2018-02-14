import pkg_resources
import os
import sys
import configparser
import json
import math
from kryptoflow.definitions import CONFIG_PATH
from datetime import datetime, time
from threading import Timer
from kryptoflow.definitions import TIMEFRAME
from time import sleep


def load_conf():
    with open(CONFIG_PATH, 'r') as inf:
        return json.load(inf)


class TimeUtils(object):
    def __init__(self):
        self._last_timestamp = datetime.now().timestamp()
        self.inital_timestamp = None

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
    def closest_timeframe(self):
        return int(TIMEFRAME * round(float(self.now)/TIMEFRAME))

    @staticmethod
    def round_up_to_timeframe(timestamp):
        return int(math.ceil(timestamp / TIMEFRAME)) * TIMEFRAME

    def round_no_nearest(self):
        return int(TIMEFRAME * round(float(self.now)/TIMEFRAME))

    def wait_until_checkpoint(self):
        time_entered = self.now
        time_to_start = self.round_up_to_timeframe(time_entered)
        print(self.now, time_to_start)
        while (self.now - time_to_start) < 0:
            sleep(0.0001)
        self.inital_timestamp = self.round_no_nearest()


class RepeatedTimer(object):

    def __init__(self, interval, func, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = func
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()
        self.canonical_timestamp = None

    def _run(self):

        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False