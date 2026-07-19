"""main parser for Kaye Python CLI"""

# fixme make cli prompt functional

from argparse import ArgumentParser

from kaye import PROGRAM_NAME

from kaye.cli.cli_http import register_cli_http_parser
from kaye.cli.cli_continue import register_cli_continue_parser
from kaye.cli.claude.main import register_cli_claude_parser

__all__ = ("cli_parser", "cli_subparser")


# parse definition  ############################################################


cli_parser = ArgumentParser(prog=PROGRAM_NAME, description=__doc__)
cli_parser.set_defaults(func=lambda _: cli_parser.print_help())
cli_subparser = cli_parser.add_subparsers(title="subcommands")

# register subcommands parsers
register_cli_continue_parser(cli_subparser)
register_cli_http_parser(cli_subparser)
register_cli_claude_parser(cli_subparser)
