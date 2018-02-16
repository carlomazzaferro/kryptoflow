import abc
from kryptoflow.services.utilities.utils import TimeUtils, RepeatedTimer
from kryptoflow.definitions import SCHEMAS
import os
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from collections import defaultdict


class Streamer(abc.ABC):

    def __init__(self, topic=None):
        super(Streamer, self).__init__()

        self.key_schema = avro.load(os.path.join(SCHEMAS, 'keyschema.avsc'))
        self.topic = topic
        self.producer = AvroProducer({'bootstrap.servers': '127.0.0.1:9092',
                                      'schema.registry.url': 'http://127.0.0.1:8081'},
                                     default_key_schema=self.key_schema,
                                     default_value_schema=avro.load(os.path.join(SCHEMAS, self.topic + '.avsc')))

        print(os.path.join(SCHEMAS, self.topic + '.avsc'))
        self.timer = RepeatedTimer
        self.time_util = TimeUtils()

    @abc.abstractmethod
    def cache(self):
        return

    @abc.abstractmethod
    def as_producer(self):
        return

    def send(self, message):
        message['ts'] = str(message['ts'])
        print(message)
        self.producer.produce(topic=self.topic, value=message)  #, key=message.keys())
        self.producer.flush()

    def _release_cache(self):
        self._accumulator = defaultdict(list)
        self._comment_accumulator = self._tweet_accumulator = {'sentences': [],
                                                               'sentence_count': 0,
                                                               'polarity': 0}


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

