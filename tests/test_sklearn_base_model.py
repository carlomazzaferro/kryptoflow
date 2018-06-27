#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.linear_model import LogisticRegression
import numpy
import pytest
from kryptoflow.skeleton import fib
X1, Y1 = make_classification(n_features=2, n_redundant=0, n_informative=1,
                             n_clusters_per_class=1)
__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "none"


@pytest.fixture
def sklearn_model():
    sample_data = numpy.array([0, 1])
    lr = LogisticRegression()



def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)


