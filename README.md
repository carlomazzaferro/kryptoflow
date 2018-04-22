Kryptoflow
==========


Algorithmic crypto trading framework with Kafka and TensorFlow ([Keras](https://keras.io/) + [TensorFlow Serving](https://www.tensorflow.org/serving/))


Description
===========

Coming soon ...

Run
===
### Infrastructure: kafka, tensorflow, et. al.

Spin up kafka and related scrapers (zookeeper, kafka-ui, etc.)

```bash
docker-compose up
```

### Services: Data Gathering 
*NOTE*: WIP, some stuff may may give errors or be less than optimally documented. 

Build the application code that will gather data and stream it to kafka
```
docker build -t kryptoflow .
docker exec -it kryptoflow bash 
```

Now you are inside the container, which contains all the code from the repo. Running:

```
python3.6 kryptoflow/scrapers/reddit.py
python3.6 kryptoflow/scrapers/twitter.py
python3.6 kryptoflow/scrapers/btcusd.py
```

Starts each service. Alternatively, run `supervisord -c resources/supervisord.conf`, and check the status
by running `supervisorctl -c resources/supervisord.conf`

### Services, without Docker (MacOS)

## Dependencies

1. python3.6
2. librdkafka: `brew install librdkafka`
3. `pip install -r requirements.txt`
4. `pip install -e .`

Then, run `supervisord -c resources/supervisord.conf`

###  Analysis
Check out Keras [training notebook](https://github.com/carlomazzaferro/kryptoflow/blob/master/keras_training.ipynb)
for training and model storing instructions

### Deploy with Tensorflow Serving

Build the docker container with bazel, tf serving, and all the required dependencies to
serve the model. This may take some time (~40 minutes)

```bash
bash kryptoflow/serving/build_server.sh 
```

Then, copy the stored models to the container:

```bash
bash kryptoflow/serving/serve.sh 1
```
 
The `1` indicates the number of the model. Check `saved_models/` directory for the available
stored models. These are automatically saved when the class `kryptoflow.ml.export.ModelExporter` is
instantiated. See the notebook for more info on how to stored the models themselves.



