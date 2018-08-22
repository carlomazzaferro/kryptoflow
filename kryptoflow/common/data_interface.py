import logging

from datetime import datetime, timedelta
import pandas
import tensorflow as tf
import numpy

from rx import Observable

from kafka_tfrx.stream import KafkaStream
from kryptoflow.ml.dataset import one_hot_encode


_logger = logging.getLogger('root')


def rows_to_df(rows, categorical=None):
    df = pandas.DataFrame(rows)
    df.index = pandas.to_datetime(df['ts'])
    df['ts'] = pandas.to_datetime(df['ts'])
    df['time_diff'] = df['ts'].diff().dt.seconds.div(1, fill_value=0)
    if categorical:
        df = one_hot_encode(df, categorical)
    df = df.drop('ts', 1)
    return df


def stream_from_start(observer):
    stream = KafkaStream.avro_consumer(topic='gdax', offset='start')
    Observable \
        .from_(stream) \
        .subscribe(observer())


def get_historic_data(offset, max_points=None):
    stream = KafkaStream.avro_consumer(topic='gdax', offset=offset)
    source = Observable \
        .from_(stream) \
        .take_while(lambda value: datetime.now() -
                                  datetime.strptime(value['ts'], '%Y-%m-%d %H:%M:%S') > timedelta(seconds=5))

    a = source.to_blocking()
    if max_points:
        return [msg for msg in a][-max_points:]

    else:
        return [msg for msg in a]


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


def training_pipeline():
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


def keras_model():
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