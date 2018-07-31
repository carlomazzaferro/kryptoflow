import os
import shutil
import pytest
from kryptoflow.managers.constants import TEMPLATE_PROJECT_FILES
from kryptoflow.managers.base import BaseConfigManager
from kryptoflow.managers.project import ProjectManager


def test_default():
    assert BaseConfigManager.IS_GLOBAL is False
    assert BaseConfigManager.KRYPTOFLOW_DIR is None
    assert BaseConfigManager.CONFIG_FILE_NAME is None
    assert BaseConfigManager.CONFIG is None


def test_project():
    assert ProjectManager.IS_GLOBAL is False
    assert ProjectManager.KRYPTOFLOW_DIR is None
    assert ProjectManager.CONFIG_FILE_NAME == 'kryptoflow.yaml'
    assert ProjectManager.CONFIG is None


def test_get_config_file_path():

    BaseConfigManager.CONFIG_FILE_NAME = 'wrongfile.yml'
    assert BaseConfigManager.get_config() is None
    assert BaseConfigManager.get_value('key') is None

    BaseConfigManager.CONFIG_FILE_NAME = 'kryptoflow.yaml'
    assert BaseConfigManager.is_initialized() is False
    assert os.path.dirname(BaseConfigManager.get_config_file_path()) == '.'

    BaseConfigManager.KRYPTOFLOW_DIR = 'tests/test-project'
    assert BaseConfigManager.is_initialized() is True
    assert os.path.basename(BaseConfigManager.get_config_file_path()) == 'kryptoflow.yaml'

    with pytest.raises(AttributeError):
        BaseConfigManager.get_value('key')

    assert isinstance(BaseConfigManager.get_config(), dict)
    assert BaseConfigManager.get_value('name') == 'test-project'

    BaseConfigManager.set_config(init=False)
    assert os.path.isfile(os.path.join(BaseConfigManager.KRYPTOFLOW_DIR, BaseConfigManager.CONFIG_FILE_NAME))
    assert 'name' in BaseConfigManager.CONFIG.keys()
    assert 'test-project' == BaseConfigManager.CONFIG['name']

    assert BaseConfigManager.set_config(init=False) is None

    BaseConfigManager.create_dir('tests/test-dir')
    assert os.path.isdir('tests/test-dir')
    shutil.rmtree('tests/test-dir')


def test_project_manager():
    ProjectManager.set_path('tests/test-project')
    assert ProjectManager.KRYPTOFLOW_DIR == 'tests/test-project'

    ProjectManager.set_path('tests/test-project-2')
    ProjectManager.create_subdirs()
    assert os.path.isdir('tests/test-project-2/kafka/logs')
    shutil.rmtree('tests/test-project-2')

    ProjectManager.set_path('tests/test-project-2')
    ProjectManager.create_template()
    for file in TEMPLATE_PROJECT_FILES:
        file_path = file.replace('template/', '')
        assert os.path.isfile(os.path.join(ProjectManager.KRYPTOFLOW_DIR, file_path))
    shutil.rmtree('tests/test-project-2')

