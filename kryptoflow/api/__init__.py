import logging
from flask import Blueprint
from flask_restplus import Api
from kryptoflow.api.endpoints.historic import ns as historic_ns
from kryptoflow.api.endpoints.live import ns as live_ns
from kryptoflow.api.endpoints.predict import ns as predict_ns
from kryptoflow.api.test import ns as test_namespace


log = logging.getLogger(__name__)

# create Flask-RestPlus API
api_bp = Blueprint('api', __name__)
api = Api(api_bp,
          version='1.0',
          title='TensorFlow Serving REST Api',
          description='RESTful API wrapper for TensorFlow Serving client')

api.add_namespace(historic_ns)
api.add_namespace(live_ns)
api.add_namespace(predict_ns)
api.add_namespace(test_namespace)


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

    from kryptoflow.managers.dashboard import DashBoardManager
    if not DashBoardManager.DEFAULT_FLASK_DEBUG:
        return {'message': message}, 500
