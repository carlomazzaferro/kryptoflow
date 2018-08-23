import os
import sys
import logging
import shutil

import click
from kryptoflow.managers.project import ProjectManager

_logger = logging.getLogger('root')


@click.command()
@click.option('--name', help='Project Name', default='make-money')
@click.option('--path', help='Path where project w', default='.')
def init(name, path):
    project_path = os.path.join(path, name)
    if os.path.isdir(project_path):
        safe_init(project_path)
    else:
        ProjectManager.create_dir(project_path)
        ProjectManager.set_path(project_path)
        ProjectManager.init_project()


def safe_init(project_path):
    overwrite = input('WARNING: Path specified already exists. Any configuration will be overwritten. Proceed?[Y/n]')
    if overwrite == 'Y':
        ProjectManager.set_path(project_path)
        ProjectManager.init_project()
    elif overwrite == 'n':
        sys.exit()
    else:
        safe_init(project_path)
