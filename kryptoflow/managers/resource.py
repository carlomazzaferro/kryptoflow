# -*- coding: utf-8 -*-

import json
import os
import logging
from datetime import datetime

from kryptoflow.managers.project import ProjectManager
from kryptoflow.managers.base import BaseConfigManager
from kryptoflow.common.validation import ResourcedError, NotInitilizedError


_logger = logging.getLogger('root')

try:
    import boto3
except ImportError:  # pragma: no cover
    _logger.warning('Boto3 not installed, backups to AWS will fail')


class ResourceManager(ProjectManager):

    @classmethod
    def backup_resources(cls):
        backup_paths = cls.get_value('backup')
        if not backup_paths:
            raise NotInitilizedError('Project must be initialized first with `kryptoflow init`')

        resources = [ResourceFactory.get_resource(k, v) for k, v in
                     backup_paths.items() if v]

        if not resources:
            _logger.warning('No resources specified, skipping backup')
        return resources

    @classmethod
    def do_backup(cls, stream):
        for backup in cls.backup_resources():
            backup.write(stream)

    @classmethod
    def get_latest_backup_time(cls):
        latest = {}
        for backup in cls.backup_resources():
            latest[backup.__class__.__name__] = fname_to_datetime(backup.get_last())
        return latest


class ResourceFactory(object):

    @classmethod
    def get_resource(cls, location, path):
        try:
            return {'AWS_bucket': S3(path), 'local': LocalDisk(path)}[location]
        except KeyError:
            raise ResourcedError(f'Resource {location} does not exists')


class LocalDisk(object):

    def __init__(self, path='kafka/backups'):
        self.path = path

    def write(self, stream):
        if not os.path.isdir(self.path):
            BaseConfigManager.create_dir(self.path)  # pragma: no cover

        with open(format_backup(self.path, stream[0]), 'w') as out:
            json.dump(stream, out, indent=4, sort_keys=True)
        _logger.info(f'Backup saved locally for data starting at: {stream[0]["ts"]}')

    def get_last(self):
        return sorted(os.listdir(self.path),
                      key=lambda x: fname_to_datetime(x),
                      reverse=True)[0]


class S3(object):

    def __init__(self, bucket='kryptoflow'):
        self.bucket = bucket
        self.client = boto3.client('s3')

    def write(self, stream):
        try:
            self.client.create_bucket(Bucket=self.bucket)
        except Exception as e:
            raise ResourcedError(e)

        self.client.put_object(
            Bucket=self.bucket,
            Body=json.dumps(stream, indent=4, sort_keys=True),
            Key=format_backup('backups', stream[0]))
        _logger.info(f'Backup saved to S3 for data starting at: {stream[0]["ts"]}')

    def get_last(self):
        objects = sorted(self.client.list_objects(Bucket=self.bucket)['Contents'],
                         key=lambda x: fname_to_datetime(fname_from_object(x)),
                         reverse=True)

        return [fname_from_object(o) for o in objects][0]


def fname_from_object(object_path):
    return os.path.basename(object_path['Key'])


def format_backup(path, message):
    return os.path.join(path, message['ts'] + '.json')


def fname_to_datetime(fname):
    return datetime.strptime(fname.split('.')[0], '%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    ProjectManager.set_path('kryptoflow/template')
    rm = ResourceManager.backup_resources()

        # ResourceManager.do_backup(chunk)

    print(ResourceManager.get_latest_backup_time())
