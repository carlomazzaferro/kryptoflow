Kryptoflow
==========


Real-time framework for crypto-related things using Kafka and TimescaleDB


Description
===========

Coming soon ....

Run
===
### Infrastructure: kafka, timescaledb, kafka connectors
```bash
docker-compose up
docker-compose run timescale-psql


docker cp resources/connector/psql-sql.properties kafka_lenses:/opt/confluent/etc/schema-registry/
docker cp resources/postgres-sink.properties kafka_lenses:/opt/confluent/etc/kafka-connect-jdbc/postgres-sink.properties

docker exec -it kryptoflow_lenses_1 connect-standalone /opt/confluent/etc/schema-registry/psql-sql.properties /opt/confluent/etc/kafka-connect-jdbc/postgres-sink.properties
```

### Services
```bash
supervisord -c resources/supervisor.conf
```
To check processes are running:

```bash
supervisorctl -c resources/supervisord.conf

```

### Dependencies

1. Docker
2. python3.6
3. `pip install -r requirements.txt`

You're set. Connect to `timescaledb` using any Postgres enabled client using 
```bash
psql -h localhost -U postgres
```
and begin your analysis.


