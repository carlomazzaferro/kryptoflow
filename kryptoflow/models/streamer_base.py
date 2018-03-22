import abc
from kryptoflow.services.utilities.utils import TimeUtils, RepeatedTimer
from kryptoflow.definitions import SCHEMAS
import os
from confluent_kafka import avro, TopicPartition
from confluent_kafka.avro import AvroProducer, AvroConsumer
from confluent_kafka import KafkaError
import confluent_kafka


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

    def read_new(self):

        self.avro_consumer.subscribe(['reddit'])

        running = True

        while running:
            msg = self.avro_consumer.poll()
            if not msg.error():
                print(msg.value())
            elif msg.error().code() != KafkaError._PARTITION_EOF:
                print(msg.error())
                running = False
        self.avro_consumer.close()

    def read_from_start(self):
        c = AvroConsumer(dict(self.base_config, **{'group.id': 'groupid',
                                                   'default.topic.config': {'auto.offset.reset': 'beginning',
                                                                            'auto.commit.enable': 'false'}
                                                   }
                              )
                         )

        c.assign([TopicPartition('reddit', partition=0, offset=confluent_kafka.OFFSET_BEGINNING)])

        counter = 0
        while True:
            counter += 1
            msg = c.poll()
            # print(msg.value())
            print(msg)


    def persist_locally(self, path, message, topic):
        pass


if __name__ == '__main__':

    a = AvroAsync(topic='reddit')
    a.read_from_start()
