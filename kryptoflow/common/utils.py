import json
import math
import sys
from kryptoflow.definitions import CONFIG_PATH
from datetime import datetime, time
import time as t
from threading import Timer
from kryptoflow.definitions import TIMEFRAME
import logging


_logger = logging.getLogger(__name__)


def load_conf():
    with open(CONFIG_PATH, 'r') as inf:
        return json.load(inf)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    level = logging.DEBUG if loglevel else logging.INFO

    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=level, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


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

    @staticmethod
    def now():
        return datetime.now()

    @property
    def closest_timeframe(self):
        return int(TIMEFRAME * round(float(self.now().timestamp())/TIMEFRAME))

    @staticmethod
    def round_up_to_timeframe(timestamp):
        return int(math.ceil(timestamp / TIMEFRAME)) * TIMEFRAME

    def round_to_nearest(self):
        return int(TIMEFRAME * round(float(self.now().timestamp())/TIMEFRAME))


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


def utc_to_local(utc_datetime):
    now_timestamp = t.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset
