Kryptoflow
==========

[![Join the chat at https://gitter.im/kryptoflow-repo/Lobby](https://badges.gitter.im/kryptoflow-repo/Lobby.svg)](https://gitter.im/kryptoflow-repo/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/carlomazzaferro/kryptoflow.svg?branch=master)](https://travis-ci.org/carlomazzaferro/kryptoflow)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/16f53461ce4740899363141d52483e7f)](https://www.codacy.com/project/carlomazzaferro/kryptoflow-serving/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kryptoflow/kryptoflow-serving&amp;utm_campaign=Badge_Grade_Dashboard)
[![Downloads](http://pepy.tech/badge/kryptoflow)](http://pepy.tech/project/kryptoflow)

Algorithmic crypto trading framework with Kafka and TensorFlow ([Keras](https://keras.io/) + [TensorFlow Serving](https://www.tensorflow.org/serving/))

Documentation live at: https://carlomazzaferro.github.io/kryptoflow/index.html

**STATUS**: pre-alpha. Very active development. Feel free to rip the code apart, repurpose it, improve on it, or
do whatever else it may please. Documentation is also not fully up to date. This will change soon.

Description
===========

The idea behind this project is to take care of the infrastructural work
that goes behind building a machine learning-driven trading systems. In particular, the aim is giving users
a working set up for:

1. Gathering as granular data as possible 
2. Test a variety of strategies intuitively and with low friction
3. Deploying models easily and keeping them up to date
4. Trading continuously and reliably


All this done through a rich API and a browser-based GUI. Want to test your newly developed deep learning model 
tplace to start. 

Another use case: want to build something like Quantopian but using cutting-edge machine learning? Then you
may need to build it yourself. Here you'll find most of the tooling needed. 

``
Installation and Requirements
=============================

Some basic requirements:

1. python3.6 
2. Docker 

More at: https://carlomazzaferro.github.io/kryptoflow/installation.html

```bash
$ pip install kryptoflow
```


Creating a New Project
======================

```bash
$ kryptoflow init --name make-money --path /home/user/projects
```

This will create all the configuration necessary to get going, alongside docker files and other stuff. Cd into the 
repo and check out its contents. 

Spinning Up Resources
=====================

From the project directory, run:

```bash
docker-compose up
```

Training and Deploying a Model
==============================

```bash
$ kryptoflow train --epocs 10 --model model.py
```

Then

```bash
$ kryptoflow serve --model-number 1
```


License
-------

[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)


