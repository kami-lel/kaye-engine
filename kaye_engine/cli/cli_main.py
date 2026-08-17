"""
main parser for Kaye Python CLI
"""

from argparse import ArgumentParser
from importlib.metadata import version

from kaye_engine import PACKAGE_NAME
from kaye_engine.cli.claude.main import register_cli_claude_parser
from kaye_engine.cli.dynamic_node.parser import register_dynamic_node_parser
from kaye_engine.cli.blueprint.main_parser import register_cli_blueprint_parser
from kaye_engine.cli.exportable_parser import register_exportable_parser

__all__ = ("register_cli_main_parser", "register_cli_subcommands")


# constants  ###################################################################
PROGRAM_NAME = "kaye-engine"


# Public API  ##################################################################
def register_cli_subcommands(cli_subparser):
    """
    register every engine-owned subcommand (``blueprint``, ``claude``, the
    dynamic-node command, the exportable command) onto an existing
    subparsers action, so sibling
    packages can compose their own top-level parser with engine's
    subcommands mixed in, instead of only being able to add to the
    subparser :func:`register_cli_main_parser` hands back

    :param cli_subparser: subparsers action to register subcommands onto
    :type cli_subparser: argparse._SubParsersAction
    """
    register_cli_blueprint_parser(cli_subparser)
    register_cli_claude_parser(cli_subparser)
    register_dynamic_node_parser(cli_subparser)
    register_exportable_parser(cli_subparser)


# Main Entry Point  ############################################################
def register_cli_main_parser(program_name=PROGRAM_NAME):
    """
    build the top-level Kaye CLI parser and register its subcommands

    :param program_name: name shown as the CLI's ``prog`` in ``--help``
            output
    :type program_name: str
    :return: top-level parser and its subparsers action
    :rtype: tuple(ArgumentParser, argparse._SubParsersAction)
    """
    parser = ArgumentParser(prog=program_name, description=__doc__)
    parser.add_argument(
        "--version",
        action="version",
        version=str(version(PACKAGE_NAME)),
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subparser = parser.add_subparsers(title="subcommands")

    register_cli_subcommands(subparser)

    return parser, subparser
