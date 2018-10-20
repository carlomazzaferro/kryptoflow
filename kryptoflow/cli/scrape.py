import os
from kryptoflow.managers.project import ProjectManager
import click
from supervisor.supervisord import main


@click.command()
@click.option('--monitor', help='Monitor scraping jobs', is_flag=True)
@click.option('--source', help='What to run',  default='all')
def scrape(monitor, source):
    """

    Parameters
    ----------
    monitor: bool
        Start supervisord monitoring server

    source: str
        'all', 'gdax', 'reddit', 'twitter'

    Returns
    -------

    """

    ProjectManager.set_path('.')
    main(['-c', os.path.join(ProjectManager.KRYPTOFLOW_DIR, ProjectManager.get_value('supervisor'))])
    if monitor:
        print('monitoring')

