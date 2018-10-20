import pkgutil
import os
from kryptoflow.common.validation import NotInitilizedError
from kryptoflow.managers.secrets import SecretsManager
from kryptoflow.managers.base import BaseConfigManager
from kryptoflow.managers.constants import TEMPLATE_PROJECT_FILES, TEMPLATE_PROJECT_DIRS


class ProjectManager(BaseConfigManager):
    """Manages project configuration kryptoflow.yaml file."""

    IS_GLOBAL = False
    KRYPTOFLOW_DIR = None
    CONFIG_FILE_NAME = 'kryptoflow.yaml'
    CONFIG = None

    @classmethod
    def set_path(cls, path):
        cls.KRYPTOFLOW_DIR = path

    @classmethod
    def init_project(cls):
        cls.init_config()
        cls.create_template()

    @classmethod
    def create_template(cls):
        cls.create_subdirs()
        for file in TEMPLATE_PROJECT_FILES:
            data = pkgutil.get_data('kryptoflow', file)
            file_path = file.replace('template/', '')
            with open(os.path.join(cls.KRYPTOFLOW_DIR, file_path), 'w') as f:
                f.write(data.decode('utf-8'))

    @classmethod
    def create_subdirs(cls):
        for path in TEMPLATE_PROJECT_DIRS:
            os.makedirs(os.path.join(cls.KRYPTOFLOW_DIR, path), exist_ok=True)

    @classmethod
    def get_models(cls):
        if not cls.is_initialized():
            raise NotInitilizedError('Project must be initialized first with `kryptoflow init`')
        models = os.listdir(cls.get_value('saved-models'))
        return sorted([int(i) for i in models if i.isnumeric()])

    @classmethod
    def get_secrets(cls, resource):
        SecretsManager.KRYPTOFLOW_DIR = cls.KRYPTOFLOW_DIR
        return SecretsManager.get_value(resource)
