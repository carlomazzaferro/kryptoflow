#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator
import os
import pytest
from sklearn.datasets import make_classification
from kryptoflow.models.model import SklearnModel, TrainableModel
import shutil
from kryptoflow.definitions import SAVED_MODELS


__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "GNU GPL v2"


@pytest.fixture
def sklearn_model():
    x, y = make_classification(n_features=2, n_redundant=0, n_informative=1, n_clusters_per_class=1)
    lr = LogisticRegression()
    lr.fit(x, y)
    return lr


@pytest.fixture
def serializer():
    skl = SklearnModel(artifact=sklearn_model)
    skl.store(name='clf')


def test_serialization(sklearn_model):
    skl = SklearnModel(artifact=sklearn_model)
    skl.store(name='clf')
    assert os.path.exists(os.path.join(skl.model_path, 'clf' + '.mdl'))
    skl.store(name='clf2')
    assert os.path.exists(os.path.join(skl.model_path, 'clf2' + '.mdl'))

    # cleanup
    for root, dirs, files in os.walk(SAVED_MODELS):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def test_mulitple_serializations(sklearn_model):
    skl1 = SklearnModel(artifact=sklearn_model)
    skl1.store(name='clf1')
    assert os.path.exists(skl1.model_path)

    skl2 = SklearnModel(artifact=sklearn_model)
    skl2.store(name='clf2')

    skl3 = SklearnModel(artifact=sklearn_model)
    skl3.store(name='clf2')
    assert len(os.listdir(SAVED_MODELS)) == 3

    # cleanup
    for root, dirs, files in os.walk(SAVED_MODELS):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def test_loader(sklearn_model):
    skl = SklearnModel(artifact=sklearn_model)
    skl.store(name='clf')
    reloaded = skl.load(name='clf')
    assert isinstance(reloaded, BaseEstimator)

    skl2 = SklearnModel(artifact=sklearn_model)
    skl2.store(name='clf')
    reload_first = skl.load(run_number=1, name='clf')
    assert isinstance(reload_first, BaseEstimator)

    for root, dirs, files in os.walk(SAVED_MODELS):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def test_trainable_model_from_file(sklearn_model):
    skl = SklearnModel(artifact=sklearn_model)
    # lr = LogisticRegression()
    # trainable = TrainableModel(artifact=lr)

    skl.store(name='clf')
    trainable = TrainableModel.from_file(run_number=1, name='clf', model_type='sklearn')
    assert isinstance(trainable.model, BaseEstimator)
    for root, dirs, files in os.walk(SAVED_MODELS):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def test_trainable_model(sklearn_model):
    assert isinstance(sklearn_model, BaseEstimator)
    trainable = TrainableModel(sklearn_model)
    assert isinstance(trainable.model, BaseEstimator)
    assert isinstance(trainable.serializer, SklearnModel)
