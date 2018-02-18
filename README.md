Kryptoflow
==========


Real-time framework for crypto-related things using Kafka and TimescaleDB


Description
===========

Coming soon ....

Run
===
### Infrastructure: kafka, timescaledb, kafka connectors

Spin up kafka and timescale
```bash
docker-compose up
```

Run the connector between both
```
docker exec -it kryptoflow_lenses_1 connect-standalone /opt/confluent/etc/schema-registry/psql-sql.properties /opt/confluent/etc/kafka-connect-jdbc/postgres-sink.properties
```

### Services
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
Connect to `timescaledb` using any Postgres enabled client using: 

```bash
psql -h localhost -U postgres
```
and begin your analysis.


