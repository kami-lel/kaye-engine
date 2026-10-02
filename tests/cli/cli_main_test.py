"""
cli_main_test.py

Unit Tests (using pytest) for:

register_cli_subcommands, register_cli_main_parser
"""

from argparse import ArgumentParser

import pytest

from kaye_engine.cli.cli_main import (
    PROGRAM_NAME,
    register_cli_main_parser,
    register_cli_subcommands,
)


# pytest  ######################################################################
class TestRegisterCliSubcommands:

    def test_registers_onto_a_caller_built_subparser(_):
        parser = ArgumentParser()
        subparser = parser.add_subparsers()

        register_cli_subcommands(subparser)

        for argv in (
            ["blueprint"],
            ["claude"],
            ["continue"],
            ["sync-open-webui-skills"],
            ["o"],
            ["skill", "-a", "F"],
            ["s", "alpha", "F"],
            ["dynamic-node", "decode-only-abbr"],
        ):
            args = parser.parse_args(argv)
            assert callable(args.func)


    def test_claude_skills_is_registered_and_singular_is_not(_):
        parser = ArgumentParser()
        subparser = parser.add_subparsers()
        register_cli_subcommands(subparser)

        for argv in (["claude", "skills"], ["claude", "s"]):
            assert callable(parser.parse_args(argv).func)

        with pytest.raises(SystemExit):
            parser.parse_args(["claude", "skill"])


class TestRegisterCliMainParser:

    def test_prog_defaults_to_program_name(_):
        parser, _subparser = register_cli_main_parser()
        assert parser.prog == PROGRAM_NAME

    def test_prog_uses_given_program_name(_):
        parser, _subparser = register_cli_main_parser(
            program_name="my-program"
        )
        assert parser.prog == "my-program"

    def test_subcommands_still_registered(_):
        parser, _subparser = register_cli_main_parser()

        for argv in (
            ["blueprint"],
            ["claude"],
            ["continue"],
            ["sync-open-webui-skills"],
            ["o"],
            ["skill", "-a", "F"],
            ["s", "alpha", "F"],
            ["dynamic-node", "decode-only-abbr"],
        ):
            args = parser.parse_args(argv)
            assert callable(args.func)
