#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import six
import pytest
from sklearn.datasets import make_classification
from tensorflow.keras import Model as KerasBaseModel
from tensorflow.keras import backend as K
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from kryptoflow.models.model import KerasModel, TrainableModel
import shutil
from kryptoflow.managers.project import ProjectManager


__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "GNU GPL v2"


def keras_test(func):
    """Function wrapper to clean up after TensorFlow tests.
    # Arguments
        func: test function to clean up after.
    # Returns
        A function wrapping the input function.
    """
    @six.wraps(func)
    def wrapper(*args, **kwargs):
        output = func(*args, **kwargs)
        K.clear_session()
        return output
    return wrapper


@pytest.fixture(scope='function')
def keras_model():
    x, y = make_classification(n_features=2, n_redundant=0, n_informative=1, n_clusters_per_class=1)
    model = Sequential()
    model.add(Dense(64, input_dim=2, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    model.fit(x, y)
    return model


@pytest.fixture
def project_manager():
    p = ProjectManager()
    p.set_path('tests/test-project')
    p.set_config(init=False)
    return p


@pytest.fixture
def serializer():
    skl = KerasModel(artifact=keras_model)
    skl.store(name='nn')


@keras_test
def test_serialization(keras_model, project_manager):
    skl = KerasModel(artifact=keras_model)
    skl.store(name='nn')
    assert os.path.exists(os.path.join(skl.model_path, 'nn' + '.h5'))
    assert os.path.exists(os.path.join(skl.model_path, 'nn' + '.json'))
    assert os.path.exists(os.path.join(skl.model_path, 'tf.txt', 'saved_model' + '.pb'))
    assert os.path.isdir(os.path.join(skl.model_path, 'tf.txt', 'variables'))

    for root, dirs, files in os.walk(project_manager.CONFIG['saved-models']):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    with open(os.path.join(project_manager.CONFIG['saved-models'], '.gitkeep'), 'w') as gitkeep:
        gitkeep.write('empty')


@keras_test
def test_mulitple_serializations_first(keras_model):
    skl1 = KerasModel(artifact=keras_model)
    skl1.store(name='nn1')
    assert os.path.exists(skl1.model_path)


@keras_test
def test_mulitple_serializations_second(keras_model):
    skl2 = KerasModel(artifact=keras_model)
    skl2.store(name='nn2')
    assert os.path.exists(skl2.model_path)


@keras_test
def test_mulitple_serializations_third(keras_model, project_manager):
    skl3 = KerasModel(artifact=keras_model)
    skl3.store(name='nn3')
    assert len(os.listdir(project_manager.CONFIG['saved-models'])) == 3 + 1  # .gitkeep

    # cleanup
    for root, dirs, files in os.walk(project_manager.CONFIG['saved-models']):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    with open(os.path.join(project_manager.CONFIG['saved-models'], '.gitkeep'), 'w') as gitkeep:
        gitkeep.write('empty')


@keras_test
def test_loader(keras_model, project_manager):
    skl = KerasModel(artifact=keras_model)
    skl.store(name='nn')
    K.clear_session()
    reloaded = skl.load(name='nn')
    assert isinstance(reloaded, KerasBaseModel)

    for root, dirs, files in os.walk(project_manager.CONFIG['saved-models']):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    with open(os.path.join(project_manager.CONFIG['saved-models'], '.gitkeep'), 'w') as gitkeep:
        gitkeep.write('empty')


@keras_test
def test_trainable_model_from_file(keras_model, project_manager):
    skl = KerasModel(artifact=keras_model)
    skl.store(name='nn')

    K.clear_session()
    trainable = TrainableModel.from_file(run_number=1, name='nn', model_type='keras')
    assert isinstance(trainable.model, KerasBaseModel)
    for root, dirs, files in os.walk(project_manager.CONFIG['saved-models']):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    with open(os.path.join(project_manager.CONFIG['saved-models'], '.gitkeep'), 'w') as gitkeep:
        gitkeep.write('empty')


@keras_test
def test_trainable_model(keras_model, project_manager):
    trainable = TrainableModel(keras_model)
    assert isinstance(trainable.model, KerasBaseModel)
    assert isinstance(trainable.serializer, KerasModel)
    for root, dirs, files in os.walk(project_manager.CONFIG['saved-models']):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    with open(os.path.join(project_manager.CONFIG['saved-models'], '.gitkeep'), 'w') as gitkeep:
        gitkeep.write('empty')
