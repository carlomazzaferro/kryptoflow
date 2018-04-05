import logging
import traceback

from flask_restplus import Api
from kryptoflow.serving import settings


log = logging.getLogger(__name__)

# create Flask-RestPlus API
api = Api(version='1.0',
          title='TensorFlow Serving REST Api',
          description='RESTful API wrapper for TensorFlow Serving client')


# define default error handler
@api.errorhandler
def default_error_handler(error):
    """
    Default error handler, if something unexpected occured
    Args:
        error: Contains specific error information

    Returns:Tuple of JSON object with error information and 500 status code

    """
    message = 'Unexpected error occured: {}'.format(error.specific)
    log.exception(message)

    if not settings.DEFAULT_FLASK_DEBUG:
        return {'message': message}, 500
