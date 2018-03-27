from kryptoflow.definitions import SCHEMAS
import os
import json
from confluent_kafka import avro, TopicPartition
from confluent_kafka.avro import AvroProducer, AvroConsumer
from confluent_kafka import KafkaError
import confluent_kafka
import time


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
                        return cache
                    if unique:
                        if msg not in cache:
                            cache.append(msg)
                    else:
                        cache.append(msg)

            elif msg.error().code() != KafkaError._PARTITION_EOF:
                print(msg.error())
                running = False
        self.avro_consumer.close()

    def read_from_start(self, persist=False, path='/'):
        c = AvroConsumer(dict(self.base_config, **{'group.id': 'groupid',
                                                   'default.topic.config': {'auto.offset.reset': 'beginning',
                                                                            'auto.commit.enable': 'false'}
                                                   }
                              )
                         )

        c.assign([TopicPartition(self.topic, partition=0, offset=confluent_kafka.OFFSET_BEGINNING)])

        if persist:
            with open(os.path.join(path, self.topic + '.txt'), 'w') as out:
                self.run_loop(c, file_object=out)
        else:
            self.run_loop(c)

    @staticmethod
    def run_loop(consumer, file_object=None):
        counter = 0
        msg_stack = []
        last_import = time.time() - 60
        while True:
            counter += 1
            msg = consumer.poll()
            print(msg.timestamp())
            if file_object:
                try:
                    encoded = json.dumps(msg.value())
                    if encoded not in msg_stack[-10:]:
                        msg_stack.append(json.dumps(msg.value()))
                except TypeError:
                    print(msg.value())

                if msg.timestamp()[1]/1000 > last_import:
                    break

            else:
                print(msg.value())

        if file_object:
            for item in msg_stack:
                file_object.write(item + '\n')


if __name__ == '__main__':

    a = AvroAsync(topic='gdax')
    a.read_from_start(persist=True)
