[![Join the chat at https://gitter.im/kryptoflow-repo/Lobby](https://badges.gitter.im/kryptoflow-repo/Lobby.svg)](https://gitter.im/kryptoflow-repo/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/carlomazzaferro/kryptoflow.svg?branch=master)](https://travis-ci.org/carlomazzaferro/kryptoflow)

An algorithmic crypto trading framework with Kafka and TensorFlow ([Keras](https://keras.io/) + [TensorFlow Serving](https://www.tensorflow.org/serving/))


### Premise

The idea behind this project is to take care of the enormous boilerplating and infrastructural work
that goes behind building a machine learning-driven trading systems. Being a very young project, it is
still in experimental stages, and much work is left to be done. This is much closer to an early alpha
than a working release, so proceed with caution!

### Current State & Future Goals

Implemented so far:

1. Data ingestion pipeline, which includes websocket streams from twitter, reddit, gdax which are saved to three separate Kafka topics.
2. Data transforms to model gdax (BTC-USD only for now) into time-series of custom timespan to which RNNs/LSTMs can be applied for time-series prediction
3. Tensorflow training and model persistance
4. Tensorflow Serving APIs exposed through a Flask endpoint. A few details are worth mentioning here. The Tensorflow Serving is actually run within a docker container, and that docker container is polled by a Flask endpoint through gRPC.

Todo:

1. Trading system 
2. Webapp functionality, namely:
  a. Twitter/Reddit sentiment (maybe add a Word Cloud?)
  b. Predictions (live and historical)
  c. Management console: kickstart retrai/deploy new model, post to GDAX
  d. Visualization of model performance
  e. Predicted gain/loss
3. Continuous training and deployment of models
4. Road map to deploying the system in a production environment


### Architecture

To get a sense of how the project is set up, visit [architecture](architecture.html)
