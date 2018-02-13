import abc
import json
from kryptoflow.services.utilities.utils import Timer
from kryptoflow.definitions import RESOURCES_PATH
import os
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from pprint import pprint


value_schema = avro.load(os.path.join(RESOURCES_PATH, 'reddit.avsc'))
key_schema = avro.load(os.path.join(RESOURCES_PATH, 'KeySchema.avsc'))


class Streamer(abc.ABC):

    def __init__(self, topic=None):
        super(Streamer, self).__init__()
        self.topic = topic
        self.producer = AvroProducer({'bootstrap.servers': '127.0.0.1:9092',
                                      'schema.registry.url': 'http://127.0.0.1:8081'},
                                     default_key_schema=avro.load(os.path.join(RESOURCES_PATH, self.topic + '.avsc')),
                                     default_value_schema=value_schema)

        print(os.path.join(RESOURCES_PATH, self.topic + '.avsc'))
        self.timer = Timer()

    @abc.abstractmethod
    def cache(self):
        return

    @abc.abstractmethod
    def as_producer(self):
        return

    def send(self, message):
        msg = json.dumps(message, ensure_ascii=False)
        pprint(message)
        self.producer.produce(topic=self.topic, value=message) #, key=message.keys())

    def _release_cache(self, timestamp):
        self.timer.last_timestamp = timestamp
        self._sentence_count = 0
        self._spread_cache = []
        self._price_cache = []
        self._message = {'sentences': [],
                         'polarity': 0,
                         'sentence_count': 0}


class MergedStream(Streamer):

    def __init__(self, stream_list):
        super().__init__()

        self.stream_list = stream_list

    def stream(self):
        return

    def cache(self):
        return

    def as_producer(self):
        return

