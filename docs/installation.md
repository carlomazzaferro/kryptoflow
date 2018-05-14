# Installation and Infrastructure

First, clone the repo: `git clone https://github.com/carlomazzaferro/krytptoflow.git` and 
navigate to its root path.


### Kafka, TensorFlow, et. al.

Spin up kafka and related scrapers (zookeeper, kafka-ui, etc.)

```bash
docker-compose up
```

### Dependencies

Ideally, create a new virtual environment. This is highly recommended for managing dependencies.

1. python3.6 (recommend installing with homebrew)
2. librdkafka: `brew install librdkafka`
3. Python requirements: `pip install -r requirements.txt`
4. NLTK requirements: `python3.6 -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"`
4. Local install: `pip install -e .`
5. Kafka IP: `export KAFKA_SERVER_IP='kafka1'`

Finally, you may need to edit your `/etc/hosts/` to be able to connect to kafka. Do so by running:

```bash
sudo nano /etc/hosts
```

and adding the following line to it:

```bash
127.0.0.1  localhost kafka1
```

This should be enough to have all the dependencies installed and the system up and running.
