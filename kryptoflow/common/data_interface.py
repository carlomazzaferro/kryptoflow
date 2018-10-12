from typing import Union, Iterable, AnyStr
import logging

from datetime import datetime, timedelta
import tensorflow as tf
import numpy

from rx import Observable

from kafka_tfrx.stream import KafkaStream


_logger = logging.getLogger('root')


class StreamFactory(object):

    STREAMS = KafkaStream.avro_consumer(topic='gdax', offset='start')

    @classmethod
    def stream_from_datetime(cls, start_time: datetime.date, stream_from: Union[Iterable, AnyStr]):
        stream = cls.STREAMS if stream_from == 'kafka' else stream_from
        return Observable \
                    .from_(stream) \
                    .filter(lambda value: datetime.strptime(value['ts'], '%Y-%m-%d %H:%M:%S') > start_time)

    @classmethod
    def stream_from_start(cls, stream_from: Union[Iterable, AnyStr]):
        stream = cls.STREAMS if stream_from == 'kafka' else stream_from
        return Observable \
                    .from_(stream)

    @classmethod
    def stream_from_offset(cls, offset, stream_from: Union[Iterable, AnyStr]):
        stream = cls.STREAMS if stream_from == 'kafka' else stream_from
        return Observable \
                    .from_(stream) \
                    .take_while(lambda value: datetime.now() -
                                              datetime.strptime(value['ts'], '%Y-%m-%d %H:%M:%S') > timedelta(seconds=5))


def gen():
    stream = KafkaStream.avro_consumer(topic='gdax', offset='start')
    for i in stream:
        print(i)
        yield (i['price'], i['volume_24h'], i['spread'], 1 if i['side'] == 'buy' else 0)


# TODO: rxpy take fixed amount of points and convert to tensorflow tensor

def make_tf_iterator():
    import tensorflow as tf
    import random

    def preprocess(inputs):
        print(inputs)
        x = tf.reshape(tf.cast(numpy.array([inputs]), tf.float32), (4, 1, 1))
        y = tf.one_hot(tf.cast(random.choice(0, 1), tf.uint8), 2)
    dataset = tf.data.Dataset.from_generator(gen, output_types=tf.float32, output_shapes=tf.TensorShape((4,1,1)))
    # value = data.make_one_shot_iterator().get_next()
    # sess = tf.txt.Session()
    # print(sess.run(value))  # (1, array([1]))
    # print(sess.run(value))  # (2, array([1, 1]))

    dataset = dataset.apply(tf.contrib.data.map_and_batch(
        preprocess, 30))
    # dataset = dataset.repeat()
    # dataset = dataset.prefetch(tf.txt.contrib.data.AUTOTUNE)

    return dataset

_EPOCHS      = 5
_NUM_CLASSES = 10
_BATCH_SIZE  = 128


def training_pipeline():  # pragma: no cover
    #
    # (x_train, y_train), (x_test, y_test) = tf.txt.keras.datasets.mnist.load_data()
    # training_set = tfdata_generator((x_train, y_train), is_training=True, batch_size=_BATCH_SIZE)
    # testing_set  = tfdata_generator((x_test, y_test), is_training=False, batch_size=_BATCH_SIZE)
    training_set = make_tf_iterator().make_one_shot_iterator()
    # #############
    # Train Model
    # #############
    model = keras_model()  # your keras model here
    model.compile('adam', 'categorical_crossentropy', metrics=['acc'])
    model.fit(
        training_set,
        epochs=10,
        verbose=1)


def keras_model():  # pragma: no cover
    from tensorflow.keras.layers import Flatten, Dense, Dropout, Input

    inputs = Input(shape=(4, 1, 1))
    x = Dense(512, activation='relu')
    x = Flatten()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    outputs = Dense(_NUM_CLASSES, activation='softmax')(x)

    return tf.keras.Model(inputs, outputs)


if __name__ == '__main__':
    training_pipeline()