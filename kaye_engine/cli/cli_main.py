"""
main parser for Kaye Python CLI
"""

from argparse import ArgumentParser

from kaye_engine import PROGRAM_NAME

from kaye_engine.cli.claude.main import register_cli_claude_parser
from kaye_engine.cli.prompt.main_parser import register_cli_prompt_parser

__all__ = ("cli_parser", "cli_subparser")


# parse definition  ############################################################


cli_parser = ArgumentParser(prog=PROGRAM_NAME, description=__doc__)
cli_parser.set_defaults(func=lambda _: cli_parser.print_help())
cli_subparser = cli_parser.add_subparsers(title="subcommands")

# register subcommands parsers
register_cli_prompt_parser(cli_subparser)
register_cli_claude_parser(cli_subparser)
