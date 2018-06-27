import os

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CONFIG_PATH = os.path.join(ROOT_DIR, 'resources/resources.json')
RESOURCES_PATH = os.path.join(ROOT_DIR, 'resources')
SCHEMAS = os.path.join(ROOT_DIR, 'resources/schemas')
APP_DIR = os.path.join(os.path.join(ROOT_DIR, 'kryptoflow/serving'))
TIMEFRAME = 8
model_dir = os.path.join(os.environ['HOME'], 'SAVED_MODELS')
if not os.path.exists(model_dir):
    os.mkdir(model_dir)
    SAVED_MODELS = model_dir
