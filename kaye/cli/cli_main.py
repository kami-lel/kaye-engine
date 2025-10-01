"""
CLI for Python module ``kaye``
"""

from argparse import ArgumentParser

from kaye import PROGRAM_NAME

__all__ = ("kaye_cli_parser", "kaye_cli_subparser")


def _kaye_cli_main(_):
    # when calling ``python -m kaye``
    kaye_cli_parser.print_help()


kaye_cli_parser = ArgumentParser(prog=PROGRAM_NAME, description=__doc__)
kaye_cli_parser.set_defaults(func=_kaye_cli_main)
kaye_cli_subparser = kaye_cli_parser.add_subparsers(title="subcommands")
