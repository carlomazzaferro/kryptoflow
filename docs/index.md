[![Join the chat at https://gitter.im/kryptoflow-repo/Lobby](https://badges.gitter.im/kryptoflow-repo/Lobby.svg)](https://gitter.im/kryptoflow-repo/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/carlomazzaferro/kryptoflow.svg?branch=master)](https://travis-ci.org/carlomazzaferro/kryptoflow)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/16f53461ce4740899363141d52483e7f)](https://www.codacy.com/project/carlomazzaferro/kryptoflow-serving/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kryptoflow/kryptoflow-serving&amp;utm_campaign=Badge_Grade_Dashboard)

An algorithmic crypto trading framework with Kafka and TensorFlow ([Keras](https://keras.io/) + [TensorFlow Serving](https://www.tensorflow.org/serving/))


### Premise


The idea behind this project is to take care of the infrastructural work
that goes behind building a machine learning-driven trading systems. In particular, the aim is giving users
a working set up for:

1. Gathering as granular data as possible 
2. Test a variety of strategies intuitively and with low friction
3. Deploying models easily and keeping them up to date
4. Trading continuously and reliably


All this done through a rich API and a browser-based GUI. Want to test your newly developed deep learning model 
on the wild crypto markets without having to do anything other than write the model itself? Then this is the 
place to start. 

Another use case: want to build something like Quantopian but using cutting-edge machine learning? Then you
may need to build it yourself. Here you'll find most of the tooling needed. 

DISCLAIMER: Still in experimental stages, and much work is left to be done.
 This is much closer to an early alpha than a working release, so proceed with caution! 


### Current State & Future Goals

Implemented so far:

1. Data ingestion pipeline, which includes websocket streams from twitter, reddit, gdax which are saved to three 
separate Kafka topics.
2. Data transforms to model gdax (BTC-USD only for now) into time-series of custom timespan to which RNNs/LSTMs can 
be applied for time-series prediction
3. Tensorflow training and model persistance
4. Tensorflow Serving APIs exposed through a Flask endpoint. A few details are worth mentioning here. 
The Tensorflow Serving is actually run within a docker container, and that docker container is polled by a Flask endpoint through gRPC.
5. CLI interface, which enables 

Todo:

1. Trading system 
2. Webapp functionality, namely:
  a. Twitter/Reddit sentiment 
  b. Predictions (live and historical)
  c. Management console: kickstart retrain/deploy new model, post to GDAX
  d. Visualization of model performance
  e. Predicted gain/loss


### Architecture

To get a sense of how the project is set up, visit [architecture](architecture.html)


### Get Started

To get going, check out the [quickstart](quickstart.html) tutorial.

To set up and install all dependencies, go to [installation requirements and setup](installation.html)