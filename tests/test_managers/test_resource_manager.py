import os

import pytest

from kryptoflow.common.validation import NotInitilizedError, ResourcedError
from kryptoflow.managers.project import ProjectManager
from kryptoflow.managers.resource import (ResourceManager,
                                          LocalDisk,
                                          S3,
                                          fname_from_object)


try:
    import boto3 as b3
except ImportError:
    b3 = None


@pytest.fixture
def data():
    test_data = [
        {'price': 6380.27, 'ts': '2018-08-21 06:21:35', 'volume_24h': 8358.59144604, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:35', 'volume_24h': 8358.71904104, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:35', 'volume_24h': 8359.71904104, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:35', 'volume_24h': 8360.71904104, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:35', 'volume_24h': 8361.27723604, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:35', 'volume_24h': 8362.27723604, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:37', 'volume_24h': 8347.36550696, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:37', 'volume_24h': 8347.66550697, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:38', 'volume_24h': 8347.06950695, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:43', 'volume_24h': 8347.07513695, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:43', 'volume_24h': 8347.07670695, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:43', 'volume_24h': 8347.08264446, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:43', 'volume_24h': 8349.09264446, 'side': 'sell'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:43', 'volume_24h': 8349.09871211, 'side': 'sell'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:43', 'volume_24h': 8349.10477976, 'side': 'sell'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:43', 'volume_24h': 8349.11417091, 'side': 'sell'},
        {'price': 6380.0, 'ts': '2018-08-21 06:21:46', 'volume_24h': 8347.07704904, 'side': 'buy'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:56', 'volume_24h': 8347.0661158, 'side': 'sell'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:56', 'volume_24h': 8347.2589971, 'side': 'sell'},
        {'price': 6380.0, 'ts': '2018-08-21 06:21:56', 'volume_24h': 8347.28029188, 'side': 'buy'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:57', 'volume_24h': 8347.08598465, 'side': 'sell'},
        {'price': 6380.0, 'ts': '2018-08-21 06:22:00', 'volume_24h': 8347.21550695, 'side': 'buy'},
        {'price': 6380.28, 'ts': '2018-08-21 06:22:00', 'volume_24h': 8347.21668217, 'side': 'buy'},
        {'price': 6380.46, 'ts': '2018-08-21 06:22:04', 'volume_24h': 8347.06809264, 'side': 'buy'}
    ]

    return [test_data[i:i+4]for i in range(0, len(test_data), 4)]


def test_get_backup_resource():
    ProjectManager.set_path(None)
    with pytest.raises(NotInitilizedError):
        ResourceManager.backup_resources()
    ProjectManager.set_path('tests/test-project')
    assert len(ResourceManager.backup_resources()) == 1
    assert isinstance(ResourceManager.backup_resources()[0], LocalDisk)


def test_do_backup(data):
    ProjectManager.set_path('tests/test-project')
    for message in data:
        ResourceManager._do_backup(message)
    local_backup_path = ResourceManager.backup_resources()[0].path
    assert len(os.listdir(local_backup_path)) == 8
    assert '2018-08-21 06:21:35.json' in os.listdir(local_backup_path)

    for f in os.listdir(local_backup_path):
        os.remove(os.path.join(local_backup_path, f))


def test_get_latest_backup(data):
    ProjectManager.set_path('tests/test-project')
    for message in data:
        ResourceManager._do_backup(message)

    assert isinstance(ResourceManager.get_latest_backups(), dict)
    assert 'LocalDisk' in ResourceManager.get_latest_backups().keys()

    local_backup_path = ResourceManager.backup_resources()[0].path
    for f in os.listdir(local_backup_path):
        os.remove(os.path.join(local_backup_path, f))


def test_resource_factory():
    with pytest.raises(ResourcedError):
        ResourceManager.get_resource('wrong', 'path')


@pytest.mark.skipif(b3 is None, reason="test requires boto3")
def test_s3_backup(data):
    s3 = S3(bucket='wrong bucket')
    with pytest.raises(ResourcedError):
        s3.write(data[0])

    with pytest.raises(Exception):
        s3.get_last()


def test_utility():
    assert fname_from_object({'Key': 'bucket/fname'}) == 'fname'
