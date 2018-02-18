#!/usr/bin/env bash

apt-get update -y && apt-get install -y software-properties-common \
   && wget -qO - 'https://packages.confluent.io/deb/4.0/archive.key' | apt-key add - \
   && add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/4.0 stable main" \
   && apt-get install -y librdkafka-dev librdkafka1 \
   && pip3.6 install -r requirements.txt \
   && python3.6 setup.py develop

