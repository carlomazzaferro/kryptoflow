from typing import Union, Iterable, AnyStr

from kryptoflow.managers.base import BaseConfigManager
from kryptoflow.managers.resource import ResourceManager
from kryptoflow.common.data_interface import StreamFactory


class DataManager(BaseConfigManager):
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    RESOURCE_MANAGER = ResourceManager()
    STREAMS = StreamFactory()

    @classmethod
    def get_first_time(cls):
        pass

    @classmethod
    def do_backup(cls, chunk: int=100, stream_from: Union[Iterable, AnyStr]='kafka'):
        last_seen = cls.RESOURCE_MANAGER.get_latest_backed_up_time()
        stream_ = cls.STREAMS.stream_from_datetime(last_seen, stream_from).buffer_with_count(chunk)
        stream_.subscribe(lambda x: cls.RESOURCE_MANAGER._do_backup(x))

    @classmethod
    def stream(cls, stream_from: Union[Iterable, AnyStr]='kafka'):
        return cls.STREAMS.stream_from_start(stream_from)

    @classmethod
    def historic_blocking(cls, stream_from: Union[Iterable, AnyStr]='kafka'):
        return cls.STREAMS.stream_from_start(stream_from).to_blocking()


if __name__ == '__main__':
    import os
    test_data = [
        {'price': 6380.27, 'ts': '2018-08-21 06:19:30', 'volume_24h': 8358.59144604, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:19:34', 'volume_24h': 8358.71904104, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:19:34', 'volume_24h': 8359.71904104, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:20:34', 'volume_24h': 8360.71904104, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:20:34', 'volume_24h': 8361.27723604, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:20:35', 'volume_24h': 8362.27723604, 'side': 'sell'},
        {'price': 6380.27, 'ts': '2018-08-21 06:20:37', 'volume_24h': 8347.36550696, 'side': 'sell'},
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

    from kryptoflow.managers.project import ProjectManager
    ProjectManager.set_path('tests/test-project')
    # print(ResourceManager.get_latest_backed_up_time())
    ResourceManager._do_backup(test_data[0:5])
    dm = DataManager
    dm.do_backup(chunk=2, stream_from=test_data)
    print(os.listdir('tests/test-project/kafka/backups'))

