import json
import pandas
import numpy
import os
from itertools import chain
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin


class ForecastTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, n_time_steps=8, prediction_steps=1):
        self.n = n_time_steps
        self.pred_steps = prediction_steps
        self.tuple_index = None

    def fit(self, X, y=None):
        """

        Args:
            X (pandas.DataFrame):
            y (pandas.Series, numpy.array):

        Returns:

        """
        top_columns = [['t_' + str(self.n - y) for x in range(self.n) for y in [x]*len(X.columns)] + ['t_0'],
                       list(X.columns)*self.n + ['target']]
        self.tuple_index = list(zip(*top_columns))
        return self

    def transform(self, X, y=None, live=False):
        data = []
        index = []
        for i, sub_df in X.groupby(numpy.arange(len(X))//self.n):

            target = sub_df['price'].values[-1]
            index.append(sub_df.index[-1])
            new_row = list(chain.from_iterable(sub_df.values.tolist())) + [target]
            data.append(new_row)

            if len(new_row) != len(self.tuple_index):
                continue

        forecasting = pandas.DataFrame(data, columns=pandas.MultiIndex.from_tuples(self.tuple_index), index=index)
        forecasting[('t_0', 'target')] = forecasting[('t_0', 'target')].shift(-self.pred_steps)
        if len(forecasting) > 1:
            forecasting = forecasting.dropna()
            return forecasting[:-self.pred_steps].values
        else:
            forecasting = forecasting.fillna(1)
            return forecasting.values


class TimeEmbedder(BaseEstimator, TransformerMixin):

    def __init__(self, inital_dims):
        """
        Transform to a time-embedded array from a single long array. I.e., group features into their
        buckets so that they actually represent data from related timestamps

        Args:
            inital_dims (int): initial dimensions of array
        """
        self.initial_dims = inital_dims
        self.middle_shape = None

    def fit(self, X, y=None):
        self.middle_shape = (X.shape[1]-1)//self.initial_dims
        return self

    def transform(self, X):
        y = X[:, -1]
        X = X[:, :-1]
        return numpy.reshape(X, (X.shape[0], self.middle_shape, self.initial_dims)), y


def get_data(source, remote=False, keep_keys=list(['ts']),
             categorical=list(['side'])):
    file_path = '/media/carlo/HDD/kafka_local/'
    file_path = os.path.join(file_path, source + '.txt')
    rows = []
    with open(file_path) as inf:
        for i, row in enumerate(inf):
            if remote:
                if i >= 8:
                    break
            row_dict = json.loads(row)
            rows.append({k: v for k, v in row_dict.items() if k in keep_keys})

    df = pandas.DataFrame(rows)
    df.index = pandas.to_datetime(df['ts'])
    df['ts'] = pandas.to_datetime(df['ts'])
    df['time_diff'] = df['ts'].diff().dt.seconds.div(1, fill_value=0)
    if categorical:
        df = one_hot_encode(df, categorical)
    df = df.drop('ts', 1)
    return df


def one_hot_encode(df, categ_vars):
    ohe = []
    for categ in categ_vars:
        ohe.append(pandas.get_dummies(df[categ]))
        df = df.drop(categ, 1)
    return pandas.concat([df] + ohe, 1)


if __name__ == '__main__':

    local_df = get_data('gdax', remote=False, keep_keys=['ts', 'price', 'volume_24h',
                                                         'spread', 'side'])  # type: pandas.DataFrame

    remote_df = get_data('gdax', remote=True, keep_keys=['ts', 'price', 'volume_24h',
                                                         'spread', 'side'])  # type: pandas.DataFrame

    pipe = Pipeline([
        ('tr', ForecastTransformer()),
        ('scaler', MinMaxScaler()),
        ('time', TimeEmbedder(inital_dims=len(local_df.columns)))
    ])

    x, y = pipe.fit_transform(local_df)

