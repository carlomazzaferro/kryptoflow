#!/usr/bin/env bash

docker build --pull -t $USER/tensorflow-serving-devel -f kryptoflow/serving/Dockerfile .
docker run -it $USER/tensorflow-serving-devel --name tf_serving