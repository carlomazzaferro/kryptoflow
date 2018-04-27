#!/usr/bin/env bash

docker cp stored_models/$1/tf tf_serving:/serving
docker start tf_serving && docker exec -it tf_serving mv /serving/tf /serving/$1
docker exec -it tf_serving /serving/bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server \
    --port=9000 --model_base_path=/serving/ &> gan_log &