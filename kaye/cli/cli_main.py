"""
cli_main.py

main parser for Kaye Python CLI
"""

# todo CLI to import/export w/ OpenWebUI
# fixme make cli functional again for prompt

from argparse import ArgumentParser

from kaye import PROGRAM_NAME

from kaye.cli.cli_http import register_cli_http_parser
from kaye.cli.cli_continue import register_cli_continue_parser
from kaye.cli.cli_claude.cli_claude_main import register_cli_claude_parser

__all__ = ("cli_parser", "cli_subparser")


# parse definition  ############################################################
def _cli_main(_):
    # when calling ``python -m kaye``
    cli_parser.print_help()


cli_parser = ArgumentParser(prog=PROGRAM_NAME, description=__doc__)
cli_parser.set_defaults(func=_cli_main)
cli_subparser = cli_parser.add_subparsers(title="subcommands")

# register subcommands parsers
register_cli_continue_parser(cli_subparser)
register_cli_http_parser(cli_subparser)
register_cli_claude_parser(cli_subparser)
