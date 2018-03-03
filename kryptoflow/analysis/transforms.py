from tsfresh import select_features
from sklearn.base import TransformerMixin, BaseEstimator
from datetime import datetime, timedelta
import pandas
from tsfresh.utilities.dataframe_functions import make_forecasting_frame


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

    def __init__(self, minutes=0, hours=0, days=0):
        self.frame_shift = timedelta(minutes=minutes, hours=hours, days=days)

    def fit(self):
        return self

    def determine_timeshift_count(self, df):
        frequency = timedelta(df.index[0] - df.index[1])
        return int(self.frame_shift/frequency)

    def transform(self, X, y=None):
        max_timeshift = self.determine_timeshift_count(X)
        return make_forecasting_frame(X["price"], kind="price", max_timeshift=max_timeshift, rolling_direction=1)
