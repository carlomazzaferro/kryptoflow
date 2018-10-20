
import yaml
import pkgutil
import os
import logging

_logger = logging.getLogger('root')


class BaseConfigManager(object):
    """Base class for managing a configuration file.
        Based on the amazing github.com/polyaxon/polyaxon config manager setup
    """

    IS_GLOBAL = False
    KRYPTOFLOW_DIR = None
    CONFIG_FILE_NAME = None
    CONFIG = None

    @staticmethod
    def create_dir(dir_path):
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except OSError:
                # Except permission denied and potential race conditions
                # in multi-threaded environments.
                _logger.error('Could not create config directory `%s`', dir_path)

    @classmethod
    def get_config_file_path(cls):
        if not cls.KRYPTOFLOW_DIR:
            # local to this directory
            base_path = os.path.join('.')
        else:
            base_path = cls.KRYPTOFLOW_DIR
        return os.path.join(base_path, cls.CONFIG_FILE_NAME)

    @classmethod
    def init_config(cls):
        cls.set_config(init=True)

    @classmethod
    def is_initialized(cls):
        config_file_path = cls.get_config_file_path()
        return os.path.isfile(config_file_path)

    @classmethod
    def set_config(cls, init=False):
        config_file_path = cls.get_config_file_path()

        if os.path.isfile(config_file_path) and init:
            _logger.debug("%s file already present at %s",
                          cls.CONFIG_FILE_NAME, config_file_path)
            return

        with open(config_file_path, "w") as config_file:
            cls.CONFIG = yaml.load(pkgutil.get_data('kryptoflow', 'template/kryptoflow.yaml'))
            cls.CONFIG['saved-models'] = os.path.join(cls.KRYPTOFLOW_DIR, cls.CONFIG['saved-models'])
            cls.CONFIG.update({'name': os.path.basename(cls.KRYPTOFLOW_DIR)})
            yaml.dump(cls.CONFIG, config_file, default_flow_style=False)

    @classmethod
    def get_config(cls):
        if not cls.is_initialized():
            return None

        config_file_path = cls.get_config_file_path()
        with open(config_file_path, "r") as config_file:
            return yaml.load(config_file)

    @classmethod
    def get_value(cls, key):
        config = cls.get_config()
        if config:
            if key in config.keys():
                return config[key]
            else:
                _logger.warning("Config `%s` has no key `%s`", cls.CONFIG.__name__, key)

        return None


