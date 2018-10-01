### Create a new project

Kryptoflow comes with a handy cli tool that enables you to perform most of the work. First thing you'd want to
do is create a new project. This assumes that kryptoflow is installed.

```bash
$ kryptoflow init --name 'test-project' --path '/home/user/projects'
```

The command will create a new projected located at `/home/user/projects/test-project`. The directory will look like this:

```bash
kafka/                          # Kafka logs, data and config files
    logs/
    count-messages.sh
    server.properties
    set_topics_config.sh
serialized/                     tf.txt
docker-compose.yaml             # Docker configuration for kafka and related services
Dockerfile.tfserving            # Docker configuration for tensorflow serving
kryptoflow.yaml                 # Project configuration
model.py                        # Keras/tensorflow model
secrets.yaml                    # API secrets for reddit, twitte, gdax
```

### Kafka, TensorFlow Serving

To spin up the required resources, simply run:

```bash
docker-compose up
```
This may take some time if running for the first time, mainly because the TensorfFlow serving 
container is quite large. 

The docker compose file also includes a UI for your Kafka topics. Head to [localhost:8000](localhost:8000) to check out Kafka's UI (provided by [Landoop](https://www.landoop.com/)).
 

### Data Ingestion

Now you can start ingesting data and storing it to Kafka. (If you find yourself wondering why the hell we are
using Kafka for this project, a few notes are available on the [architecture](architecture.html) page).

From your project root directory, you can simply run:

```bash
$ kryptoflow scrape --monitor
```

Obviously, it may take some time until you have enough data to do some meaningful work, but luckily
kryptoflow has its own in-built mechanisms to ensure the data ingestion won't stop. We use [supervisor](https://github.com/Supervisor/supervisor)
alongside with a few failover mechanisms to ensure data is continuously ingested. 

To verify that your data is being ingested appropriatley, head to [http://localhost:8000](http://localhost:8000) for a visual ui of the Kafka
topics being ingested.

### Model Training

The file `model.py` contains a baseline TensorFlow model for you to start playing around with. 

```bash
$ kryptoflow train --epocs 10 --model model.py
```

Will kickstart the training process. At the end of the training session, the model will be automatically
serialized, and a version will be assigned to it. You can see all the version trained so far in 
the `/serialized` directory. 


### Model Serving


```bash
$ kryptoflow serve --model-number 1
```

This will place the serialized model inside the tensorflow serving container and expose a REST 
interface through which it can be called


## To be continued
