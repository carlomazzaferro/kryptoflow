import click
import logging
from kryptoflow.models.model import ServableModel

__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "none"

_logger = logging.getLogger('root')


@click.command()
@click.option('--model-number', default='latest', help='Number of epochs.')
def serve(model_number):
    """
    docker run -it $USER/tensorflow-serving-devel --name tf_serving
    docker cp stored_models/$1/tf tf_serving:/serving
    docker start tf_serving && docker exec -it tf_serving mv /serving/tf /serving/$1
    docker exec -it tf_serving /serving/bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server \
        --port=9000 --model_base_path=/serving/ &> gan_log &
    Args:
        model_number:
    Returns:
    """
    servable = ServableModel(model_number=model_number, model_type='keras')
    servable.copy_to_container()
    servable.serve()