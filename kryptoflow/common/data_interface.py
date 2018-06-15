import os
import logging

from datetime import datetime, timedelta
import pandas
from keras import backend as K
from keras.models import model_from_json
from sklearn.externals import joblib
from tensorflow.python.saved_model import builder as saved_model_builder, tag_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def
from rx import Observable, Observer

from kryptoflow.definitions import SAVED_MODELS
from kafka_tfrx.stream import KafkaStream
from kryptoflow.ml.dataset import one_hot_encode


_logger = logging.getLogger('root')


def rows_to_df(rows, categorical=list([])):
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
    source = Observable \
        .from_(stream) \
        .subscribe(observer())


def get_historic_data(offset, max_points=50000):
    stream = KafkaStream.avro_consumer(topic='gdax', offset=offset)
    source = Observable \
        .from_(stream) \
        .take_while(lambda value: datetime.now() -
                                  datetime.strptime(value['ts'], '%Y-%m-%d %H:%M:%S') > timedelta(seconds=5))

    a = source.to_blocking()
    return [msg for msg in a][-max_points:]


class ModelImporter(object):

    def __init__(self, model_type='sklearn', latest=True, number=1):
        self.type = model_type
        self.latest = latest
        if self.latest:
            existing_models = sorted([int(i) for i in os.listdir(SAVED_MODELS)])
            self.number = existing_models[-1]
        else:
            self.number = number
        self.model_path = os.path.join(SAVED_MODELS, str(self.number), self.type)

    def load(self, name):
        if self.type == 'sklearn':
            return joblib.load(os.path.join(self.model_path, name + '.mdl'))
        elif self.type == 'keras':
            json_model_file = open(os.path.join(self.model_path, name + '.json'), "r").read()
            loaded_model = model_from_json(json_model_file)
            loaded_model.load_weights(os.path.join(self.model_path, name + '.h5'))


class ModelExporter(object):
    """
    Save model as:
        - json
        - Weights: .h5 files;
        - Protobuf: for loading into TensorFlow Serving
        - Checkpoints: also for TF Serving

    The models will live in the directory `stored_models/i/` where i is an integer which is assigned automatically.
    Within that directory, there will be a `tf` and a `keras` directory, where each of the versions of the serialized
    model will be stored.
    """
    def __init__(self):
        """
        Args:
            model (keras.Model): compiled keras model
        """
        self.models_dir = os.path.join(SAVED_MODELS, str(self.path_id))
        os.mkdir(self.models_dir)

    def store(self, model, name, model_type='keras'):
        if model_type == 'sklearn':
            self._store_sklearn(name, model)
        else:
            self._store_keras(name, model)
            self._store_tf(name)

    @property
    def path_id(self):
        existing_models = sorted([int(i) for i in os.listdir(SAVED_MODELS)])
        return existing_models[-1] + 1

    @property
    def sklearn_model_path(self):
        return os.path.join(self.models_dir, 'sklearn')

    @property
    def keras_model_path(self):
        return os.path.join(self.models_dir, 'keras')

    @property
    def tf_model_path(self):
        return os.path.join(self.models_dir, 'tf')

    def _store_sklearn(self, name, model):
        os.mkdir(self.sklearn_model_path)
        joblib.dump(model, os.path.join(self.sklearn_model_path, name + '.mdl'))
        _logger.info("Saved sklearn model to disk")

    def _store_keras(self, name, model):
        K.set_learning_phase(0)  # necessary to prevent model from modifying weights
        os.makedirs(self.keras_model_path)
        model_json = model.to_json()
        with open(os.path.join(self.keras_model_path, name + '.json'), 'w') as json_file:
            json_file.write(model_json)
        model.save_weights(os.path.join(self.keras_model_path, name + '.h5'))
        _logger.info("Saved Keras model to disk")

    def _store_tf(self, name):

        json_model_file = open(os.path.join(self.keras_model_path, name + '.json'), "r").read()
        loaded_model = model_from_json(json_model_file)
        loaded_model.load_weights(os.path.join(self.keras_model_path, name + '.h5'))

        builder = saved_model_builder.SavedModelBuilder(self.tf_model_path)
        signature = predict_signature_def(inputs={'states': loaded_model.input},
                                          outputs={'price': loaded_model.output})

        with K.get_session() as sess:
            builder.add_meta_graph_and_variables(sess=sess,
                                                 tags=[tag_constants.SERVING],
                                                 signature_def_map={'predict': signature})
            builder.save()

        _logger.info("Saved tf model to disk")
