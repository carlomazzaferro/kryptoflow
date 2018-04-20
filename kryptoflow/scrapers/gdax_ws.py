import gdax
from datetime import datetime
from kryptoflow.common.streamer_base import AvroAsync
from kryptoflow.scrapers.utilities.utils import utc_to_local


class GDAXClient(gdax.WebsocketClient):

    def __init__(self, products=None, channels=None, producer=None):

        super(GDAXClient, self).__init__(products=products, channels=channels)
        self.topic = 'gdax'
        self.url = "wss://ws-feed.gdax.com/ticker"
        self.producer = producer

    def on_message(self, message):
        if self.validate_msg(message):
            return
        else:
            message = self._format_message(message)
            self.producer.produce(topic=self.topic, value=message)

            self.producer.flush()

    def start_stream(self):
        try:
            self.start()
        except Exception as e:
            print('ERRROR', e)
            self.start_stream()

    @staticmethod
    def validate_msg(msg):
        if any([i not in msg.keys() for i in ['price', 'time', 'best_ask', 'best_bid']]):
            return True
        else:
            return False

    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/ticker"
        self.products = ["BTC-USD"]

    @staticmethod
    def calculate_spread(msg):
        return abs(float(msg['best_bid']) - float(msg['best_ask']))

    def _format_message(self, message):
        msg = {'price': float(message['price']),
               'ts': str(
                   utc_to_local(
                       datetime.strptime(message['time'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(microsecond=0)
                   )
               ),
               'volume_24h': float(message['volume_24h']),
               'spread': self.calculate_spread(message),
               'side': message['side']}
        print(msg)

        return msg

    def on_close(self):
        print("-- Goodbye! --")


if __name__ == '__main__':

    sink = AvroAsync(topic='gdax')
    gd = GDAXClient(products=['BTC-USD'], channels=['ticker'], producer=sink.producer())
    gd.start_stream()