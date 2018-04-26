from kryptoflow import __version__
import argparse
import sys
import logging

_logger = logging.getLogger(__name__)


def parse_common_args():
    parser = argparse.ArgumentParser(
        description="Common Kryptoflow argument parser",
        add_help=False)

    parser.add_argument(
        '-v',
        '--verbose',
        dest='loglevel',
        help='set loglevel to INFO',
        action='store_const',
        const=logging.INFO)

    parser.add_argument(
        '--version',
        action='version',
        version='kryptoflow {ver}'.format(ver=__version__))
    return parser


def parse_start_args(args):
    parent_parser = parse_common_args()
    parser = argparse.ArgumentParser(
        description='Train model using Kryptoflow',
        parents=[parent_parser])

    parser.add_argument(
        '--scrape',
        help='Start automatically scraping gdax, reddit, twitter',
        action='store_true')

    return parser.parse_args(args)


def parse_train_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parent_parser = parse_common_args()
    parser = argparse.ArgumentParser(
        description='Train model using Kryptoflow',
        parents=[parent_parser])

    parser.add_argument(
        '--epochs',
        help='Number of epochs through which the model will be trained',
        type=int,
        default=10,
        metavar='EPOCHS')

    parser.add_argument(
        '--val-split',
        help='Validation split used to check model performance. Float between 0 and 1',
        default=0.8,
        type=float,
        metavar='SPLIT')

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")
