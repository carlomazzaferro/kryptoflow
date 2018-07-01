import abc
import os
import joblib
from kryptoflow.serializer.model_io import ModelExporter, ModelImporter
from kryptoflow.models import conf
from kryptoflow.definitions import SAVED_MODELS
import logging
from typing import Type, Union
from sklearn.base import BaseEstimator
from keras.engine.training import Model as KerasBaseModel
from keras import backend as K
from keras.models import model_from_json
from tensorflow.python.saved_model import builder as saved_model_builder, tag_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

_logger = logging.getLogger('root')


class Model(object):

    def __init__(self, model_type='sklearn'):
        existing_models = sorted([int(i) for i in os.listdir(SAVED_MODELS)])
        if not existing_models:
            self._number = 1
        else:
            self._number = existing_models[-1] + 1
        self._type = model_type

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = number

    @property
    def model_type(self):
        return self._type

    @property
    def model_path(self):
        return os.path.join(SAVED_MODELS, str(self.number), self.model_type)


class SklearnModel(Model):

    def __init__(self, artifact=None):
        super().__init__(model_type='sklearn')
        self.arifact = artifact

    def load(self, run_number: Union[str, int]='last', name: str='clf'):
        """
        Load a scikit-learn model from pickled instance

        Args:
            run_number: 'last' or integer value representing the run number
            name: name of the model

        Returns: scikit learn representation of the model

        """
        if run_number is not 'last':
            self.number = str(run_number)

        return joblib.load(os.path.join(self.model_path, name + '.mdl'))

    def store(self, name: str='clf') -> None:
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump(self.arifact, os.path.join(self.model_path, name + '.mdl'))
        _logger.info("Saved sklearn model to disk")


class KerasModel(Model):
    def __init__(self, artifact=None):
        super().__init__(model_type='keras')
        self.artifact = artifact

    def load(self, run_number: Union[str, int]='last', name: str='sklearn'):
        """
        Load a keras/tf model from pickled instance

        Args:
            run_number: 'last' or integer value representing the run number
            name: name of the model

        Returns: scikit learn representation of the model

        """
        if run_number is not 'last':
            self.number = str(run_number)

        json_model_file = open(os.path.join(self.model_path, name + '.json'), "r").read()
        loaded_model = model_from_json(json_model_file)
        loaded_model.load_weights(os.path.join(self.model_path, name + '.h5'))
        return loaded_model

    def store(self, name: str='nn') -> None:
        os.makedirs(self.model_path, exist_ok=True)
        with K.get_session() as sess:
            self._store_keras(name)
            self._store_tf(name, sess)

    def _store_keras(self, name):

        K.set_learning_phase(0)  # necessary to prevent model from modifying weights
        model_json = self.artifact.to_json()
        with open(os.path.join(self.model_path, name + '.json'), 'w') as json_file:
            json_file.write(model_json)

        self.artifact.save_weights(os.path.join(self.model_path, name + '.h5'))
        _logger.info("Saved Keras model to disk")

    def _store_tf(self, name, session):

        json_model_file = open(os.path.join(self.model_path, name + '.json'), "r").read()

        loaded_model = model_from_json(json_model_file)

        loaded_model.load_weights(os.path.join(self.model_path, name + '.h5'))

        builder = saved_model_builder.SavedModelBuilder(os.path.join(self.model_path, 'tf'))
        signature = predict_signature_def(inputs={'states': loaded_model.input},
                                          outputs={'price': loaded_model.output})


        builder.add_meta_graph_and_variables(sess=session,
                                             tags=[tag_constants.SERVING],
                                             signature_def_map={'predict': signature})
        builder.save()

        _logger.info("Saved tf model to disk")


class TrainableModel(object):

    def __init__(self, artifact: Union[KerasBaseModel, BaseEstimator]):
        self.model = artifact
        if isinstance(self.model, KerasBaseModel):
            model_type = 'keras'
        elif isinstance(self.model, BaseEstimator):
            model_type = 'sklearn'
        else:
            raise ValueError('Model must be either a Keras complied model or an sklearn model')

        self.serializer = {'sklearn': SklearnModel(), 'keras': KerasModel()}[model_type]

    def train(self, x_train, y_train):
        pass

    @classmethod
    def from_file(cls, run_number: Union[str, int]='last', name: str='clf', model_type: str='sklearn'):
        if model_type not in conf.ALLOWABLE_MODLES:
            raise ValueError('Model type must either of: %s' % ', '.join(conf.ALLOWABLE_MODLES))
        serializer = {'sklearn': SklearnModel(), 'keras': KerasModel()}[model_type]
        return cls(artifact=serializer.load(run_number, name))


class ServableModel(Model):
    pass