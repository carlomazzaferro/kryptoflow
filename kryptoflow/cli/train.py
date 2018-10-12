import click
import logging


__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "none"

_logger = logging.getLogger('root')


def load():
    pass
    # remote_df = data_interface.get_historic_data(offset='start', max_points=None)
    # pipe = Pipeline([
    #
    #     ('tr', dataset.ForecastTransformer()),
    #     ('scaler', MinMaxScaler()),
    #     ('time', dataset.TimeEmbedder(inital_dims=len(remote_df.columns)))
    # ])
    #
    # x, y = pipe.fit_transform(remote_df)
    # exp.store(pipe, 'pipeline', model_type='sklearn')
    # return x, y


@click.command()
@click.option('--epochs', default=10, help='Number of epochs.')
@click.option('--split', default=0.8, help='Train-test split')
@click.option('--model-dir', help='Location where models will be serialized', required=False)
def train(split, epochs):
    x, y = load()
    split_length = int(len(x)*split)
    x, y = x[0:split_length], y[0:split_length]
    x_val, y_val = x[split_length:], y[split_length:]
    keras_model = model.KerasModel(dims=x.shape[1:])
    keras_model.fit(x, y, x_val, y_val, epochs=epochs)
    exp.store(keras_model.model, 'base', model_type='keras')




