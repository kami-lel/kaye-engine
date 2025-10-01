"""
CLI for Python module ``kaye``
"""

from argparse import ArgumentParser

from kaye import PROGRAM_NAME
from kaye.cli.cli_prompt_main import register_cli_prompt_parser

__all__ = ("cli_parser", "cli_subparser")


def _cli_main(_):
    # when calling ``python -m kaye``
    cli_parser.print_help()


cli_parser = ArgumentParser(prog=PROGRAM_NAME, description=__doc__)
cli_parser.set_defaults(func=_cli_main)
cli_subparser = cli_parser.add_subparsers(title="subcommands")

register_cli_prompt_parser(cli_subparser)
