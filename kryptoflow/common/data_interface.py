import json
import os

import pandas
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from kryptoflow import definitions
from kryptoflow.common.streamer_base import AvroAsync
from kryptoflow.ml.dataset import one_hot_encode, TimeEmbedder, ForecastTransformer


def get_data(topic, keep_keys=list(['ts']), categorical=list(['side'])):

    consumer = AvroAsync(topic=topic)
    data = consumer.read_from_start(return_msgs=True)
    # data = consumer.read_from_offset(1010393)
    print(len(data))
    rows = [{k: v for k, v in msg.items() if k in keep_keys} for msg in data]

    df = pandas.DataFrame(rows)
    df.index = pandas.to_datetime(df['ts'])
    df['ts'] = pandas.to_datetime(df['ts'])
    df['time_diff'] = df['ts'].diff().dt.seconds.div(1, fill_value=0)
    if categorical:
        df = one_hot_encode(df, categorical)
    df = df.drop('ts', 1)
    return df


def accumulate_data(time_steps=definitions.TIMEFRAME):
    consumer = AvroAsync(topic='gdax')
    messages = consumer.read_new(accumulate=True, n_messages=time_steps, unique=True)
    return messages


if __name__ == '__main__':

    # local_df = get_data('gdax', remote=False, keep_keys=['ts', 'price', 'volume_24h',
    #                                                      'spread', 'side'])  # type: pandas.DataFrame

    remote_df = get_data('gdax', keep_keys=['ts', 'price', 'volume_24h', 'spread', 'side'])  # type: pandas.DataFrame

    pipe = Pipeline([
        ('tr', ForecastTransformer()),
        ('scaler', MinMaxScaler()),
        ('time', TimeEmbedder(inital_dims=len(remote_df.columns)))
    ])

    x, y = pipe.fit_transform(remote_df)
    print(x, y)
    print(x.shape, y.shape)

