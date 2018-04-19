#!/usr/bin/env bash

# Changes config to keep topics forever

docker exec -it kryptoflow_kafka1_1 kafka-topics --alter --topic twitter --zookeeper zoo1:2181  --config 'retention.ms=120960000000' --config 'segment.ms=120960000000'
docker exec -it kryptoflow_kafka1_1 kafka-topics --alter --topic gdax --zookeeper zoo1:2181  --config 'retention.ms=120960000000' --config 'segment.ms=120960000000'
docker exec -it kryptoflow_kafka1_1 kafka-topics --alter --topic reddit --zookeeper zoo1:2181  --config 'retention.ms=120960000000 ' --config 'segment.ms=120960000000'



