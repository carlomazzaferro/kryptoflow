
class Config:
    DEBUG = False
    TESTING = False
    DEFAULT_FLASK_SERVER_NAME = '0.0.0.0'
    DEFAULT_FLASK_SERVER_PORT = 8000

    # client settings
    DEFAULT_TF_SERVER_NAME = '172.17.0.2'
    DEFAULT_TF_SERVER_PORT = 9000
    TF_MODEL_NAME = 'default'
    TF_MODEL_SIGNATURE_NAME = 'helpers'
    TF_MODEL_INPUTS_KEY = 'states'


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False


class TestConfig(Config):
    TESTING = True


config_by_name = dict(
    dev=DevConfig,
    test=TestConfig,
    prod=ProdConfig
)
