"""
Borrowed and adapted from the amazing: https://becominghuman.ai/creating-restful-api-to-tensorflow-models-c5c57b692c10
"""

import logging.config
from flask import Flask, Blueprint, render_template, send_from_directory
from flask_cors import CORS
from kryptoflow.serving.backend import utils, settings
from kryptoflow.serving.backend.api.restplus import api
from kryptoflow.serving.backend.api.predict.endpoints.client import ns as prediction_namespace
from kryptoflow.serving.backend.api.historical.endpoints.client import ns as historic_namespace
from kryptoflow.serving.backend.api.test import ns as test_namespace
from flask_socketio import SocketIO
from kryptoflow.serving.backend.ws.handler import AvroListener, thread

# create Flask application
app = Flask(__name__)
            # static_folder=settings.STATIC_FILES_DIR,
            # template_folder=settings.EMEBER_DIST)


CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app)


# load logging confoguration and create log object
logging.config.fileConfig('kryptoflow/serving/backend/logging.conf')
log = logging.getLogger(__name__)


@app.route('/')
def index():
    return send_from_directory(settings.EMEBER_DIST, "index.html")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory(settings.EMEBER_DIST, "index.html")


@socketio.on('connect')
def test_connection():

    global thread
    print(thread.is_alive())
    # Start the random number generator thread only if the thread has not been started before.
    if not thread.is_alive():
        thread = AvroListener(socketio)
        thread.start()


def __get_flask_server_params__():
    '''
    Returns connection parameters of the Flask application
    :return: Tripple of server name, server port and debug settings
    '''
    server_name = utils.get_env_var_setting('FLASK_SERVER_NAME', settings.DEFAULT_FLASK_SERVER_NAME)
    server_port = utils.get_env_var_setting('FLASK_SERVER_PORT', settings.DEFAULT_FLASK_SERVER_PORT)

    flask_debug = utils.get_env_var_setting('FLASK_DEBUG', settings.DEFAULT_FLASK_DEBUG)
    flask_debug = True if flask_debug == '1' else False

    return server_name, server_port, flask_debug


def configure_app(flask_app, server_name, server_port):
    '''
    Configure Flask application
    :param flask_app: instance of Flask() class
    '''
    flask_app.config['SERVER_NAME'] = server_name + ':' + server_port
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app, server_name, server_port):
    '''
    Initialize Flask application with Flask-RestPlus
    :param flask_app: instance of Flask() class
    '''

    prediction = Blueprint('tf_api', __name__, url_prefix='/tf_api')

    configure_app(flask_app, server_name, server_port)
    api.init_app(prediction)
    api.add_namespace(prediction_namespace)
    api.add_namespace(historic_namespace)
    api.add_namespace(test_namespace)
    flask_app.register_blueprint(prediction)


def main():
    server_name, server_port, flask_debug = __get_flask_server_params__()
    initialize_app(app, server_name, server_port)
    log.info(
        '>>>>> Starting TF Serving client at http://{}/ >>>>>'.format(app.config['SERVER_NAME'])
    )
    # app.run(debug=flask_debug, host=server_name, port=5000)
    socketio.run(app, debug=flask_debug, host=server_name, port=5000)


if __name__ == '__main__':
    main()