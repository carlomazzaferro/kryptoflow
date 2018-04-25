from kryptoflow.definitions import SCHEMAS
import logging
import os
import json
from confluent_kafka import avro, TopicPartition
from confluent_kafka.avro import AvroProducer, AvroConsumer
from confluent_kafka import KafkaError
import confluent_kafka
import time


_logger = logging.getLogger('root')


class AvroAsync(object):

    def __init__(self, topic=None):
        self.topic = topic
        self.ip = os.environ['KAFKA_SERVER_IP']
        self.base_config = {'bootstrap.servers': self.ip + ':9092',
                            'schema.registry.url': 'http://' + self.ip + ':8081'}

        self.avro_consumer = AvroConsumer(dict(self.base_config, **{'group.id': 'groupid'}))

        self.avro_consumer.assign([TopicPartition(self.topic, 0)])
        self.key_schema = avro.load(os.path.join(SCHEMAS, 'keyschema.avsc'))
        self.value_schema = avro.load(os.path.join(SCHEMAS, self.topic + '.avsc'))

    def producer(self):
        return AvroProducer({'bootstrap.servers': 'localhost:9092',
                             'schema.registry.url': 'http://localhost:8081'},
                            default_key_schema=self.key_schema,
                            default_value_schema=self.value_schema)

    def read_new(self, accumulate=False, n_messages=8, unique=True):

        self.avro_consumer.subscribe([self.topic])
        running = True

        cache = []
        while running:
            msg = self.avro_consumer.poll()
            if not msg.error():
                print(msg.value())
                if accumulate:
                    if len(cache) >= n_messages:
                        self.avro_consumer.close()
                        return cache
                    if unique:
                        if msg not in cache:
                            cache.append(msg.value())
                    else:
                        cache.append(msg.value())

            elif msg.error().code() != KafkaError._PARTITION_EOF:
                print(msg.error())
                running = False
        self.avro_consumer.close()

    def read_from_start(self, persist=False, return_msgs=True, path='/'):
        _logger.debug('Reading data from Kafka from start...')
        c = AvroConsumer(dict(self.base_config, **{'group.id': 'groupid',
                                                   'default.topic.config':
                                                       {'auto.offset.reset': 'beginning',
                                                        'auto.commit.enable': 'false'}
                                                   }
                              )
                         )

        c.assign([TopicPartition(self.topic, partition=0, offset=confluent_kafka.OFFSET_BEGINNING)])

        if persist:
            with open(os.path.join(path, self.topic + '.txt'), 'w') as out:
                self.run_loop(c, file_object=out)
        else:
            return self.run_loop(c, return_message=return_msgs)

    def read_from_offset(self, offset=1000):
        c = AvroConsumer(dict(self.base_config, **{'group.id': 'groupid-1',
                                                   'default.topic.config': {'auto.offset.reset': 'beginning',
                                                                            'auto.commit.enable': 'false'}
                                                   }
                              )
                         )

        c.assign([TopicPartition(self.topic, partition=0, offset=offset)])
        return self.run_loop(c, return_message=True, file_object=False)

    @staticmethod
    def run_loop(consumer, file_object=None, return_message=False):
        _logger.debug('Kakfa consumer initialized, looping through data...')
        counter = 0
        msg_stack = []
        last_import = time.time() - 60
        while True:
            if counter % 10000:
                _logger.debug('Read {} messages from Kafka'.format(counter))
            counter += 1
            msg = consumer.poll(timeout=3)
            if file_object or return_message:
                try:
                    msg_stack.append(msg.value())
                except TypeError:
                    print(msg.value())

                if msg.timestamp()[1]/1000 > last_import:
                    break
            else:
                print(msg)

        if file_object:
            for item in msg_stack:
                file_object.write(json.dumps(item) + '\n')

        if return_message:
            return msg_stack

        print(counter)