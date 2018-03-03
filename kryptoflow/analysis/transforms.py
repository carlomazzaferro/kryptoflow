from tsfresh import select_features
from sklearn.base import TransformerMixin, BaseEstimator
from datetime import datetime, timedelta
import pandas


class FeatureExtractor(TransformerMixin, BaseEstimator):

    def __init__(self):
        pass

    def fit(self, X):
        return self

    def transform(self, X):
        pass


class FrameCompressor(TransformerMixin, BaseEstimator):

    def __init__(self, seconds=0, minutes=0, hours=0, days=0):
        self.timeshift = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
        self.dfs = []
        self.tss = []

    def fit_transform(self, X, y=None, **fit_params):
        for group in X.groupby(freq=pandas.Timedelta(self.timeshift)):
            mean_df = group[1].mean()

            if mean_df.isnull().any():
                self.dfs.append(self.dfs[-1])
                self.tss.append(group[0])
            else:
                self.dfs.append(group[1].mean())
                self.tss.append(group[0])

        return pandas.concat(self.dfs, axis=1, keys=self.tss).T


class FrameRoller(TransformerMixin, BaseEstimator):

    def __init__(self):
        pass