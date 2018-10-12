from threading import Thread, Event
from confluent_kafka import KafkaError
from kafka_tfrx.stream import KafkaStream
from kryptoflow.common.observers import BaseObserver
from rx import Observable

thread = Thread()
thread_stop_event = Event()


class Emitter(BaseObserver):
    def __init__(self, ws):
        self.ws = ws
        super().__init__()

    def on_next(self, value):
        if not value.error():
            print(value)
            self.ws.emit('price_event', value) # , namespace='live')

        elif value.error().code() != KafkaError._PARTITION_EOF:
            running = False


class AvroListener(Thread):
    def __init__(self, socket_client, topic='gdax'):

        self.ws = socket_client
        self.delay = 1
        self.stream = KafkaStream.consumer(topic='gdax', offset='end')
        self.source = Observable.from_(self.stream)

        super(AvroListener, self).__init__()

    def on_next(self, value):
        pass

    def listen(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """

        print('listening to kafka')

        self.source.subscribe(Emitter(self.ws))

    def run(self):
        self.listen()
