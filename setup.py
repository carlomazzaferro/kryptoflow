#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for kryptoflow.

    This file was generated with PyScaffold 3.0.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: http://pyscaffold.org/
"""

import sys
from setuptools import setup, find_packages

# Add here console scripts and other entry points in ini-style format
entry_points = """
[console_scripts]
# script_name = kafka_tfrx.module:function
# For example:
# fibonacci = kafka_tfrx.skeleton:run
"""


def setup_package():
    setup(entry_points=entry_points,
          version='0.2.1',
          install_requires=[
              'confluent-kafka==0.11.4',
              'rx==1.6.1',
              'tweepy',
              'ws4py',
              'praw',
              'pandas',
              'git+git://github.com/Supervisor/supervisor',
              'git+git://github.com/danpaquin/gdax-python',
              'nltk',
              'tweet-preprocessor==0.5.0',
              'tensorflow',
              'scikit-learn',
              'sortedcontainers',
              'kafka-tfrx'],
          tests_require=['pytest', 'pytest-cov', 'pytest-runner'],
          packages=find_packages())


if __name__ == "__main__":
    setup_package()
