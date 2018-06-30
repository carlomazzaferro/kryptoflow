#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator
import os
import pytest
from sklearn.datasets import make_classification
from kryptoflow.models.model import SklearnModel
import shutil
from kryptoflow.definitions import SAVED_MODELS


__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "GNU GPL v2"


@pytest.fixture
def cleanup():
    for root, dirs, files in os.walk(SAVED_MODELS):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


@pytest.fixture
def sklearn_model():
    x, y = make_classification(n_features=2, n_redundant=0, n_informative=1, n_clusters_per_class=1)
    lr = LogisticRegression()
    lr.fit(x, y)
    return lr


@pytest.fixture
def serializer():
    skl = SklearnModel(artifact=sklearn_model)
    skl.store(name='sklearn')


def test_serialization(sklearn_model):
    skl = SklearnModel(artifact=sklearn_model)
    skl.store(name='sklearn')
    assert os.path.exists(os.path.join(skl.model_path, 'sklearn' + '.mdl'))
    skl.store(name='sklearn_2')
    assert os.path.exists(os.path.join(skl.model_path, 'sklearn_2' + '.mdl'))

    # cleanup
    for root, dirs, files in os.walk(SAVED_MODELS):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def test_mulitple_serializations(sklearn_model):
    skl1 = SklearnModel(artifact=sklearn_model)
    skl1.store(name='sklearn1')
    assert os.path.exists(skl1.model_path)

    skl2 = SklearnModel(artifact=sklearn_model)
    skl2.store(name='sklearn1')

    skl3 = SklearnModel(artifact=sklearn_model)
    skl3.store(name='sklearn1')
    assert len(os.listdir(SAVED_MODELS)) == 3

    # cleanup
    for root, dirs, files in os.walk(SAVED_MODELS):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def test_loader(sklearn_model):
    skl = SklearnModel(artifact=sklearn_model)
    skl.store(name='sklearn')
    reloaded = skl.load(name='sklearn')
    assert isinstance(reloaded, BaseEstimator)

    skl2 = SklearnModel(artifact=sklearn_model)
    skl2.store(name='sklearn')
    reload_first = skl.load(run_number=1, name='sklearn')
    assert isinstance(reload_first, BaseEstimator)

    for root, dirs, files in os.walk(SAVED_MODELS):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))