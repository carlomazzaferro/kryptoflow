
import click
from kryptoflow.common.utils import setup_logging
from kryptoflow.cli.train import train
from kryptoflow.cli.serve import serve
from kryptoflow.cli.scrape import scrape
from kryptoflow.cli.version import version
from kryptoflow.cli.init import init


@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False, help='Turn on debug logging')
@click.pass_context
def cli(context, verbose):
    """ Polyaxon CLI tool to:
        * Parse, Validate, and Check Polyaxonfiles.
        * Interact with Polyaxon server.
        * Run and Monitor experiments.
    Check the help available for each command listed below.
    """
    setup_logging(verbose)


cli.add_command(train)
cli.add_command(serve)
cli.add_command(scrape)
cli.add_command(version)
cli.add_command(init)
# cli.add_command(tensorboard)
# cli.add_command(notebook)
# cli.add_command(dashboard)
