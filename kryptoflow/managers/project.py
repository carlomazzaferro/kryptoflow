import pkgutil
import os
from kryptoflow.managers.base import BaseConfigManager
from kryptoflow.managers.constants import TEMPLATE_PROJECT_FILES


class ProjectManager(BaseConfigManager):
    """Manages project configuration .polyaxonproject file."""

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
        os.makedirs(os.path.join(cls.KRYPTOFLOW_DIR, 'kafka/logs'))