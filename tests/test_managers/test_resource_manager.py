from kryptoflow.managers.base import BaseConfigManager
from kryptoflow.managers.project import ProjectManager
from kryptoflow.managers.resource import ResourceManager


def test_get_backup_resource():
    ProjectManager.set_path('tests/test-project')
    assert BaseConfigManager.is_initialized() is True
    # assert ResourceManager.s3() ==