from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
import logging
import sys
from . import dataset
from . import data_interface
from . import model
from .utils import parse_train_args, setup_logging

__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "none"

_logger = logging.getLogger('root')


exp = data_interface.ModelExporter()


def load():

    remote_df = data_interface.get_data('gdax', keep_keys=['ts', 'price', 'volume_24h', 'spread', 'side'])  # type: pandas.DataFrame
    pipe = Pipeline([
        ('tr', dataset.ForecastTransformer()),
        ('scaler', MinMaxScaler()),
        ('time', dataset.TimeEmbedder(inital_dims=len(remote_df.columns)))
    ])

    x, y = pipe.fit_transform(remote_df)
    exp.store(pipe, 'pipeline', model_type='sklearn')
    return x, y


def train(split=0.8, epochs=10):
    x, y = load()
    split_length = int(len(x)*split)
    x, y = x[0:split_length], y[0:split_length]
    x_val, y_val = x[split_length:], y[split_length:]
    keras_model = model.KerasModel(dims=x.shape[1:])
    keras_model.fit(x, y, x_val, y_val, epochs=epochs)
    exp.store(keras_model.model, 'base', model_type='keras')


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_train_args(args)
    setup_logging(args.loglevel)
    train(args.val_split, args.epochs)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == '__main__':
    run()

