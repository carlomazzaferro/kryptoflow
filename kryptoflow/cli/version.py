import kryptoflow
import click
import logging


_logger = logging.getLogger('root')


@click.command()
def version():
    logging.info('Kryptoflow version: ' + kryptoflow.__version__)
