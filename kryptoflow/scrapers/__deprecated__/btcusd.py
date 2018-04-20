from kryptoflow.common.streamer_base import Streamer
from datetime import datetime
import gdax
from collections import defaultdict


class GDAXClient(Streamer, gdax.WebsocketClient):

    def __init__(self, topic):

        super(GDAXClient, self).__init__(topic=topic)
        self._last_timestamp = datetime.now().timestamp()
        self.channels = ['ticker']
        self._accumulator = defaultdict(list)
        self._last_message = None

    def as_producer(self):
        pass

    def cache(self):
        pass

    def start_stream(self):
        try:
            self.channels = ['ticker']
            self.start()
        except Exception as e:
            print('ERRROR', e)
            self.channels = ['ticker']
            self.start_stream()

    @staticmethod
    def validate_msg(msg):
        print(msg.keys())
        if any([i not in msg.keys() for i in ['price', 'best_ask', 'best_bid']]):
            return False
        else:
            return True

    def accumulate(self, msg):
        if self.validate_msg(msg):
            self._accumulator['price_cache'].append(float(msg['price']))
            self._accumulator['spread_cache'].append(self.calculate_spread(msg))
            self._accumulator['volume_24h_cache'].append(float(msg['volume_24h']))

    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/ticker"
        self.products = ["BTC-USD"]

        timer_func = self.timer(5, self._send_and_release)
        timer_func.start()
        print("Lets count the messages!")

    @staticmethod
    def calculate_spread(msg):
        return abs(float(msg['best_bid']) - float(msg['best_ask']))

    @staticmethod
    def avg(values):
        return sum(values)/len(values)

    def _send_and_release(self):
        msssg = self.format_message(self._accumulator)
        self._release_cache()
        self.send(msssg)

    def on_message(self, msg):
        print(msg)
        self.accumulate(msg)

    def safe_avg(self, message, _key):
        try:
            return self.avg(message[_key])
        except ZeroDivisionError:
            return self._last_message[_key.replace('_cache', '')]

    def format_message(self, message):

        msg = {'price': self.safe_avg(message, 'price_cache'),
               'ts': str(datetime.fromtimestamp(self.time_util.round_to_nearest())),
               'volume_24h': self.safe_avg(message, 'volume_24h_cache'),
               'spread': self.safe_avg(message, 'spread_cache')}

        self._last_message = msg
        return msg

    def on_close(self):
        print("-- Goodbye! --")


if __name__ == '__main__':
    wsClient = GDAXClient(topic='gdax')
    wsClient.start_stream()