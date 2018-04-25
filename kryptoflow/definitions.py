import os

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CONFIG_PATH = os.path.join(ROOT_DIR, 'resources/resources.json')
RESOURCES_PATH = os.path.join(ROOT_DIR, 'resources')
SCHEMAS = os.path.join(ROOT_DIR, 'resources/schemas')
SAVED_MODELS = os.path.join(ROOT_DIR, 'stored_models')
APP_DIR = os.path.join(os.path.join(ROOT_DIR, 'kryptoflow/serving'))
TIMEFRAME = 8