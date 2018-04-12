## TensorFlow Serving client hosted by Flask web framework
Flask Web Server + TensorFlow Serving communicating through gRPC. TensorFlow model is hosted within a docker container. 
Use:

`bash serving/resources/build_server.sh`

To build the docker image with the model and all TF dependencies.

Then:

`bash serving/resources/serve.sh`

To actually expose a port so that flask can communicate with it. 