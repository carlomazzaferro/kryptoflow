import os
import pytest

from kryptoflow.managers.data import DataManager
from kryptoflow.managers.resource import ResourceManager
from kryptoflow.managers.project import ProjectManager


@pytest.fixture
def data():
    test_data = [
        {'price': 6380.27, 'ts': '2018-08-21 06:21:30', 'volume_24h': 8358.59144604, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:31', 'volume_24h': 8358.71904104, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:32', 'volume_24h': 8359.71904104, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:33', 'volume_24h': 8360.71904104, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:34', 'volume_24h': 8361.27723604, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:35', 'volume_24h': 8362.27723604, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:37', 'volume_24h': 8347.36550696, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:37', 'volume_24h': 8347.66550697, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:38', 'volume_24h': 8347.06950695, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:43', 'volume_24h': 8347.07513695, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:44', 'volume_24h': 8347.07670695, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:45', 'volume_24h': 8347.08264446, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:21:46', 'volume_24h': 8349.09264446, 'side': 'sell'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:47', 'volume_24h': 8349.09871211, 'side': 'sell'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:48', 'volume_24h': 8349.10477976, 'side': 'sell'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:49', 'volume_24h': 8349.11417091, 'side': 'sell'},
        {'price': 6380.0, 'ts': '2018-08-21 06:21:50', 'volume_24h': 8347.07704904, 'side': 'buy'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:51', 'volume_24h': 8347.0661158, 'side': 'sell'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:52', 'volume_24h': 8347.2589971, 'side': 'sell'},
        {'price': 6380.0, 'ts': '2018-08-21 06:21:53', 'volume_24h': 8347.28029188, 'side': 'buy'},
        {'price': 6379.99, 'ts': '2018-08-21 06:21:57', 'volume_24h': 8347.08598465, 'side': 'sell'},
        {'price': 6380.0, 'ts': '2018-08-21 06:22:00', 'volume_24h': 8347.21550695, 'side': 'buy'},
        {'price': 6380.28, 'ts': '2018-08-21 06:22:01', 'volume_24h': 8347.21668217, 'side': 'buy'},
        {'price': 6380.46, 'ts': '2018-08-21 06:22:04', 'volume_24h': 8347.06809264, 'side': 'buy'}
    ]

    return test_data


def test_do_backup(data):
    ProjectManager.set_path('tests/test-project')
    # print(ResourceManager.get_latest_backed_up_time())
    ResourceManager._do_backup(data[0:5])
    dm = DataManager
    dm.do_backup(chunk=5, stream_from=data)
    bdup_files = [i for i in os.listdir('tests/test-project/kafka/backups') if i.endswith('json')]
    assert len(bdup_files) == 5
