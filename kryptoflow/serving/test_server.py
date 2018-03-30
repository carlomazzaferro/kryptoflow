
import time
import numpy

from argparse import ArgumentParser

# Communication to TensorFlow server via gRPC
from grpc.beta import implementations
import tensorflow as tf

# TensorFlow serving stuff to send messages
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from tensorflow.contrib.util import make_tensor_proto


def parse_args():
    parser = ArgumentParser(description="Request a TensorFlow server for a prediction on the image")
    parser.add_argument("-s", "--server",
                        dest="server",
                        default='localhost:9000',
                        help="prediction service host:port")
    parser.add_argument("-arr", "--array",
                        dest="array",
                        default="",
                        help="array of state",)
    args = parser.parse_args()

    host, port = args.server.split(':')
    test_data = numpy.reshape(numpy.array([[0.94623656, 0., 0.28971311, 0.10714286, 1., 0.],
                             [0.94623131, 0., 0.29129852, 0.20338983, 0., 1.],
                             [0.94623628, 0., 0.29129529, 0., 1., 0.],
                             [0.94623628, 0., 0.29129671, 0.04761905, 1., 0.],
                             [0.94624153, 0., 0.29130193, 0., 1., 0.],
                             [0.94624153, 0.00128238, 0.29128065, 0.03508772, 1., 0.],
                             [0.94889795, 0.11002445, 0.29125366, 0., 1., 0.],
                             [0.94891911, 0., 0.29134335, 0.01587302, 1., 0.]]), (1, 8, 6))

    return host, port, test_data


def main():
    # parse command line arguments
    host, port, test_data = parse_args()

    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    # Send request
    # See prediction_service.proto for gRPC request/response details.

    start = time.time()

    request = predict_pb2.PredictRequest()

    # Call GAN model to make prediction on the image
    request.model_spec.name = 'base'
    request.model_spec.signature_name = 'predict'
    print(test_data.shape)
    request.inputs['states'].CopyFrom(make_tensor_proto(test_data, dtype=tf.float32))

    result = stub.Predict(request, 60.0)  # 60 secs timeout

    end = time.time()
    time_diff = end - start

    print(result)
    print('time elapased: {}'.format(time_diff))


if __name__ == '__main__':
    main()