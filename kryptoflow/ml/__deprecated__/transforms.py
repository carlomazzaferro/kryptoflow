from tsfresh import select_features
from sklearn.base import TransformerMixin, BaseEstimator
from datetime import datetime, timedelta
import pandas
from tsfresh.utilities.dataframe_functions import make_forecasting_frame
from tsfresh.transformers import RelevantFeatureAugmenter
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def unzip(X, y):
    if isinstance(X, tuple):
        x = X[0]
        y = X[1]
        return x, y
    else:
        return X, y


class FrameCompressor(PickleBaseTransformer):
    def __init__(self, seconds=0, minutes=0, hours=0, days=0, **kwargs):
        super(FrameCompressor, self).__init__(**kwargs)

        self.timeshift = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
        self.dfs = []
        self.tss = []

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for group in X.groupby(pandas.Grouper(freq=pandas.Timedelta(self.timeshift))):
            mean_df = group[1].mean()

            if mean_df.isnull().any():
                self.dfs.append(self.dfs[-1])
                self.tss.append(group[0])
            else:
                self.dfs.append(group[1].mean())
                self.tss.append(group[0])

        return pandas.concat(self.dfs, axis=1, keys=self.tss).T


class FrameRoller(PickleBaseTransformer):
    def __init__(self, minutes=0, hours=0, days=0, **kwargs):
        super(FrameRoller, self).__init__(**kwargs)

        self.frame_shift =  timedelta(minutes=minutes, hours=hours, days=days)
        self.y = None

    def fit(self, X, y=None):
        return self

    def determine_timeshift_count(self, df):
        frequency = pandas.Timedelta(df.index[1] - df.index[0])
        return int(self.frame_shift/frequency)

    def transform(self, X, y=None):
        max_timeshift = self.determine_timeshift_count(X)
        x, y = make_forecasting_frame(X["price"], kind="price", max_timeshift=max_timeshift, rolling_direction=1)
        return x, y


class FeatureExtractor(TransformerMixin, BaseEstimator):

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X, y = unzip(X, y)
        return extract_features(X, column_id="id", column_sort="time", column_value="value", impute_function=impute,
                                show_warnings=False), y


class PCAForPandas(PCA):
    """
    From: https://github.com/blue-yonder/tsfresh/blob/master/notebooks/perform-PCA-on-extracted-features.ipynb
    This class is just a small wrapper around the PCA estimator of sklearn including normalization to make it
    compatible with pandas DataFrames.
    """

    def __init__(self, **kwargs):
        self._z_scaler = StandardScaler()
        super(self.__class__, self).__init__(**kwargs)

        self._X_columns = None

    def fit(self, X, y=None):
        X, y = unzip(X, y)
        X = self._prepare(X)
        self._z_scaler.fit(X.values, y)
        z_data = self._z_scaler.transform(X.values, y)

        return super(self.__class__, self).fit(z_data, y)

    def fit_transform(self, X, y=None):
        """Call the fit and the transform method of this class."""
        X, y = unzip(X, y)
        X = self._prepare(X)
        self.fit(X, y)
        return self.transform(X, y)

    def transform(self, X, y=None):
        X, y = unzip(X, y)
        X = self._prepare(X)
        z_data = self._z_scaler.transform(X.values, y)

        transformed_ndarray = super(self.__class__, self).transform(z_data)

        pandas_df = pandas.DataFrame(transformed_ndarray)
        pandas_df.columns = ["pca_{}".format(i) for i in range(len(pandas_df.columns))]

        return pandas_df, y

    def _prepare(self, X):
        X.sort_index(axis=1, inplace=True)
        self._X_columns = list(X.columns)
        return X
