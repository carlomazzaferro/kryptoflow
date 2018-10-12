import os

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

from kryptoflow.managers.project import ProjectManager
from kryptoflow.managers.base import BaseConfigManager
from kryptoflow.managers.app_config import config_by_name
from kryptoflow.common.validation import NotInitilizedError
from kryptoflow.api import api_bp


class DashBoardManager(BaseConfigManager):

    DEFAULT_FLASK_SERVER_NAME = '0.0.0.0'
    DEFAULT_FLASK_SERVER_PORT = 5000
    DEFAULT_FLASK_DEBUG = False

    # client settings
    DEFAULT_TF_SERVER_NAME = '172.17.0.2'
    DEFAULT_TF_SERVER_PORT = 9000
    TF_MODEL_NAME = 'default'
    TF_MODEL_SIGNATURE_NAME = 'helpers'
    TF_MODEL_INPUTS_KEY = 'states'

    @classmethod
    def create_app(cls, env):
        app = Flask(__name__,
                    static_folder=cls.static_files_dir,
                    template_folder=cls.react_dist_dir)

        CORS(app, resources={r"/*": {"origins": "*"}})
        socketio = SocketIO(app)
        app.config.from_object(config_by_name[env])
        app.register_blueprint(api_bp, url_prefix='/api/v1')

        @app.route('/')
        def index():
            return send_from_directory(cls.static_files_dir, "index.html")

        @app.route('/<path:path>')
        def catch_all(path):
            return send_from_directory(cls.react_dist_dir, "index.html")

        return app

    @classmethod
    def run(cls, host, port, env):
        app = cls.create_app(env)
        app.run(host, port)

    @property
    def static_files_dir(self):
        if BaseConfigManager.is_initialized():
            return os.path.join(ProjectManager.KRYPTOFLOW_DIR, 'dist/assets')
        else:
            raise NotInitilizedError('Project not initialized')

    @property
    def react_dist_dir(self):
        if BaseConfigManager.is_initialized():
            return os.path.join(ProjectManager.KRYPTOFLOW_DIR, 'dist')
        else:
            raise NotInitilizedError('Project not initialized')


