#!/usr/bin/env bash

# USAGE: (sudo) bash count_messages.sh reddit

docker exec -it kryptoflow_kafka1_1 kafka-run-class kafka.tools.GetOffsetShell --broker-list \
        localhost:9092 --topic $1 --time -1 --offsets 1 | \
        awk -F ':' '{sum += $3} END {print sum}'