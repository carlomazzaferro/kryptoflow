from rx import Observable, Observer
from kryptoflow.definitions import TIMEFRAME


class BaseObserver(Observer):

    def on_next(self, value):
        print(value)

    def on_completed(self):
        print("Done!")

    def on_error(self, error):
        print("Error Occurred: {0}".format(error))


class Streamer(BaseObserver):
    """
    >>> from kryptoflow.common.stream import KafkaStream
    >>> stream = KafkaStream.consumer(topic='gdax', ip='45.55.53.47', offset='end')
    >>> source = Observable.from_(stream)

    >>> source.subscribe(Streamer())
    """

    def on_next(self, value):
        return value


class Accumulator(BaseObserver):
    """
    >>> from kryptoflow.common.stream import KafkaStream
    >>> stream = KafkaStream.consumer(topic='gdax', ip='45.55.53.47', offset='end')
    >>> source = Observable.from_(stream)

    >>> source.subscribe(Accumulator())
    """
    ACCUMULATED = []

    def on_next(self, value):

        self.ACCUMULATED.append(value)
        if len(self.ACCUMULATED) >= TIMEFRAME:
            cache = self.ACCUMULATED
            self.ACCUMULATED = []
            return cache
