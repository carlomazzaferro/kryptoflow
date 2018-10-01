import pkgutil
import os
from kryptoflow.common.validation import NotInitilizedError
from kryptoflow.managers.base import BaseConfigManager
from kryptoflow.managers.constants import TEMPLATE_PROJECT_FILES


class DataManager(BaseConfigManager):
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def get_first_time(cls):
        pass

    @classmethod
    def get_existing_data(cls):
        existing_data = cls.get_value('backup')
