import logging
import sys
import subprocess
import os
from kryptoflow import definitions
from . import dataset
from . import data_interface
from . import model
from . import app
from .utils import parse_start_args, setup_logging


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_start_args(args)
    setup_logging(args.loglevel)
    if args.scrape:
        subprocess.run(['supervisord', '-c', os.path.join(definitions.RESOURCES_PATH, 'supervisord.conf')])
    app.main()


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == '__main__':
    run()

