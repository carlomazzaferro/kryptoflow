Kryptoflow
==========


Algorithmic crypto trading framework with Kafka and TensorFlow ([Keras](https://keras.io/) + [TensorFlow Serving](https://www.tensorflow.org/serving/))


Description
===========

Coming soon ...

Run
===
### Infrastructure: kafka, tensorflow, et. al.

Spin up kafka and related services (zookeeper, kafka-ui, etc.)

```bash
docker-compose up
```

### Services: Data Gathering 
Build the application code that will gather data and stream it to kafka
```
docker build -t kryptoflow .
docker exec -it kryptoflow bash 
```

Now you are inside the container, which contains all the code from the repo. Running:

```
python3.6 kryptoflow/services/reddit.py
python3.6 kryptoflow/services/twitter.py
python3.6 kryptoflow/services/btcusd.py
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
Check out Keras [training notebook: 

