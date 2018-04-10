from threading import Thread, Event
from confluent_kafka import KafkaError
from kryptoflow.models.streamer_base import AvroAsync


thread = Thread()
thread_stop_event = Event()


class AvroListener(Thread):
    def __init__(self, socket_client, topic='gdax'):
        self.ws = socket_client
        self.delay = 1
        self.listener = AvroAsync(topic=topic)

        super(AvroListener, self).__init__()

    def listen(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """

        print('listening to kafka')
        self.listener.avro_consumer.subscribe([self.listener.topic])
        while not thread_stop_event.is_set():
            msg = self.listener.avro_consumer.poll()
            if not msg.error():
                self.ws.emit('price_event', msg.value())

            elif msg.error().code() != KafkaError._PARTITION_EOF:
                running = False

    def run(self):
        self.listen()