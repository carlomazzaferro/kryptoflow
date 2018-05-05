import logging
from kryptoflow.serving.backend import utils, settings
from kryptoflow.definitions import TIMEFRAME
import tensorflow as tf
import numpy

# Communication to TensorFlow server via gRPC
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from kryptoflow.common.data_interface import accumulate_data, ModelImporter

log = logging.getLogger(__name__)
importer = ModelImporter(model_type='sklearn', latest=True)
transformer_pipeline = importer.load('pipeline')


def _inv_transf(x):
    x -= transformer_pipeline.named_steps['scaler'].min_[-1]
    x /= transformer_pipeline.named_steps['scaler'].scale_[-1]
    return x


def _tf_server_connection_params():
    server_name = utils.get_env_var_setting('TF_SERVER_NAME', settings.DEFAULT_TF_SERVER_NAME)
    server_port = utils.get_env_var_setting('TF_SERVER_PORT', settings.DEFAULT_TF_SERVER_PORT)

    return server_name, server_port


def _create_prediction_request(image):
    # create predict request
    request = predict_pb2.PredictRequest()

    request.model_spec.name = settings.TF_MODEL_NAME
    request.model_spec.signature_name = settings.TF_MODEL_SIGNATURE_NAME
    request.inputs[settings.TF_MODEL_INPUTS_KEY].CopyFrom(
        tf.contrib.util.make_tensor_proto(image, dtype=tf.float32)
    )

    return request


def _open_tf_server_channel(server_name, server_port):
    channel = implementations.insecure_channel(
        server_name,
        int(server_port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    return stub


def _make_prediction_and_prepare_results(stub, request):
    result = stub.Predict(request, 60.0)  # 60 secs timeout
    result = numpy.array(result.outputs['price'].float_val)
    return {'val': str(_inv_transf(result))}


def _load_and_transform_data():
    remote_df = accumulate_data(time_steps=settings.TIMEFRAME)
    x, y = transformer_pipeline.transform(remote_df)
    return x


def make_prediction(state):
    # get TensorFlow server connection parameters
    server_name, server_port = _tf_server_connection_params()
    log.info('Connecting to TensorFlow server %s:%s', server_name, server_port)

    # open channel to tensorflow server
    stub = _open_tf_server_channel(server_name, server_port)

    # create predict request
    request = _create_prediction_request(state)

    # make prediction
    return _make_prediction_and_prepare_results(stub, request)
