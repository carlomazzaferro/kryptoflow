import time
import ciso8601
from kryptoflow.models.streamer_base import Streamer
from datetime import datetime
from pprint import pprint
import gdax


class GDAXClient(Streamer, gdax.WebsocketClient):

    def __init__(self, topic):

        super(GDAXClient, self).__init__()
        self.topic = topic
        self._last_timestamp = datetime.now().timestamp()
        self._price_cache = []
        self._spread_cache = []
        self.channels = ['ticker']

    def as_producer(self):
        pass

    def cache(self):
        pass

    def stream(self):
        pass

    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD"]
        print("Lets count the messages!")

    @staticmethod
    def calculate_spread(msg):
        return abs(float(msg['best_bid']) - float(msg['best_ask']))

    @staticmethod
    def avg(values):
        return sum(values)/len(values)

    def on_message(self, msg):
        if 'time' in msg.keys():
            timestamp = ciso8601.parse_datetime(msg['time']).timestamp()
            if timestamp - self.timer.last_timestamp > 5:
                try:
                    msg['price'] = self.avg(self._price_cache)
                    msg['spread'] = self.avg(self._spread_cache)
                except ZeroDivisionError:
                    msg['spread'] = self.calculate_spread(msg)

                self.send(self.format_message(msg))
                self._release_cache(timestamp)

            else:
                if 'price' in msg.keys():
                    self._price_cache.append(float(msg['price']))
                    self._spread_cache.append(self.calculate_spread(msg))

    def format_message(self, message):
        msg = {'price': float(message['price']),
               'timestamp': self.timer.closest_fith,
               'volume_24h': message['volume_24h'],
               'spread': message['spread']}

        msg = {'payload': msg, 'schema': {'type': 'struct',
                                          'name': 'btc_usd',
                                          'fields': [{"field": "price", "type": "float"},
                                                     {'field': 'volume_24h', 'type': 'float'},
                                                     {'field': 'spread', 'type': 'float'},
                                                     {'field': 'timestamp', 'type': 'float'}]
                                          }
               }

        return msg



    def on_close(self):
        print("-- Goodbye! --")


if __name__ == '__main__':

    wsClient = GDAXClient(topic='gdax')
    wsClient.start()
