import os
from kryptoflow.definitions import TIMEFRAME, APP_DIR

# Flask settings
DEFAULT_FLASK_SERVER_NAME = '0.0.0.0'
DEFAULT_FLASK_SERVER_PORT = '5000'
DEFAULT_FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# GAN client settings
DEFAULT_TF_SERVER_NAME = '172.17.0.2'
DEFAULT_TF_SERVER_PORT = 9000
TF_MODEL_NAME = 'default'
TF_MODEL_SIGNATURE_NAME = 'predict'
TF_MODEL_INPUTS_KEY = 'states'

# Model Settings
TIMES_STEPS = TIMEFRAME
DIST_FILES_DIR = os.path.join(APP_DIR, 'dist')
EMEBER_DIST = os.path.join(APP_DIR, 'frontend/dist')
STATIC_FILES_DIR = os.path.join(APP_DIR, 'frontend/dist/assets')


