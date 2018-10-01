import os
from kryptoflow.managers.project import ProjectManager
import subprocess
import click


@click.command()
@click.option('--monitor', help='Monitor scraping jobs', is_flag=True)
def dashboard(monitor):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """

    subprocess.run(['supervisord', '-c', os.path.join(ProjectManager.get_value('supervisor'), 'supervisord.conf')])
    print(monitor)
    if monitor:
        print('monitoring')
