from kryptoflow.definitions import SCHEMAS
import logging
import os
from confluent_kafka import avro, TopicPartition
from confluent_kafka.avro import AvroProducer, AvroConsumer
from confluent_kafka import KafkaError
import confluent_kafka
import uuid


_logger = logging.getLogger('root')


class IterateStream(type):

    def __iter__(cls):
        while True:
            msg = cls.avro_consumer.poll()
            if msg is not None:
                if not msg.error():

                    if msg.value() == '':
                        continue
                    else:
                        yield msg.value()

                elif msg.error().code() != KafkaError._PARTITION_EOF:
                    yield msg.error()

    def __next__(self):
        pass


class KafkaStream(metaclass=IterateStream):

    __metaclass__ = IterateStream

    CONFIG = {'start': {'group.id': 'groupid',
                        'default.topic.config': {'auto.offset.reset': 'beginning',
                                                 'auto.commit.enable': 'false'}},
              'end': {'group.id': 'groupid'}
              }

    OFFSETS = {'start': confluent_kafka.OFFSET_BEGINNING,
               'end': confluent_kafka.OFFSET_END}

    KEY_SCHEMA = avro.load(os.path.join(SCHEMAS, 'keyschema.avsc'))
    VALUE_SCHEMA = {'gdax': avro.load(os.path.join(SCHEMAS, 'gdax' + '.avsc')),
                    'reddit': avro.load(os.path.join(SCHEMAS, 'reddit' + '.avsc')),
                    'twitter': avro.load(os.path.join(SCHEMAS, 'twitter' + '.avsc'))}

    @classmethod
    def producer(cls, topic='gdax'):
        ip = cls.determine_ip()
        return AvroProducer({'bootstrap.servers': ip + ':9092',
                             'schema.registry.url': 'http://' + ip + ':8081'},
                            default_key_schema=cls.KEY_SCHEMA[topic],
                            default_value_schema=cls.VALUE_SCHEMA)

    @classmethod
    def consumer(cls, topic='gdax', offset='start'):
        ip = cls.determine_ip()
        try:
            _offset = cls.OFFSETS[offset]
            _config = cls.CONFIG[offset]
        except KeyError:
            _config = cls.CONFIG['end']
            _offset = offset

        print(_offset, _config)
        cls.avro_consumer = AvroConsumer(dict({'bootstrap.servers': ip + ':9092',
                                               'schema.registry.url': 'http://' +ip + ':8081'},

                                              **{'group.id': str(uuid.uuid1()).split('-')[0],
                                                 'default.topic.config': {'auto.offset.reset': 'beginning',
                                                                          'auto.commit.enable': 'false'}
                                                              }))
        cls.avro_consumer.assign([TopicPartition(topic, partition=0, offset=_offset)])

        return cls

    @staticmethod
    def determine_ip():
        try:
            return os.environ['KAFKA_SERVER_IP']
        except KeyError:
            return 'localhost'


