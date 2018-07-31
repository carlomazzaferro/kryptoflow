import subprocess
import os
from kryptoflow import definitions
import click


@click.command()
@click.option('--monitor', help='Monitor scraping jobs', is_flag=True)
def scrape(monitor):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """

    subprocess.run(['supervisord', '-c', os.path.join(definitions.RESOURCES_PATH, 'supervisord.conf')])
    print(monitor)
    if monitor:
        print('monitoring')
