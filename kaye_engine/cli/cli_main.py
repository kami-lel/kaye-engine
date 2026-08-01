"""
main parser for Kaye Python CLI
"""

from argparse import ArgumentParser

from kaye_engine.cli.claude.main import register_cli_claude_parser
from kaye_engine.cli.prompt.main_parser import register_cli_prompt_parser

__all__ = ("cli_parser", "cli_subparser", "register_cli_main_parser")


# constants  ###################################################################
PROGRAM_NAME = "kaye-engine"


# Main Entry Point  ############################################################
def register_cli_main_parser(program_name=PROGRAM_NAME):
    """
    build the top-level Kaye CLI parser and register its subcommands

    :param program_name: name shown as the CLI's ``prog`` in ``--help``
            output
    :type program_name: str
    :return: the top-level parser and its subparser group
    :rtype: tuple
    """
    parser = ArgumentParser(prog=program_name, description=__doc__)
    parser.set_defaults(func=lambda _: parser.print_help())
    subparser = parser.add_subparsers(title="subcommands")

    register_cli_prompt_parser(subparser)
    register_cli_claude_parser(subparser)

    return parser, subparser


cli_parser, cli_subparser = register_cli_main_parser()
