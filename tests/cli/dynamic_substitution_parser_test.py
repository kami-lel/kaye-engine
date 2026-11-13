"""
dynamic_substitution_parser_test.py

Unit Tests (using pytest) for:

_dynamic_substitution_main, register_dynamic_substitution_parser
"""

import logging
from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.cli import dynamic_substitution_parser
from kaye_engine.prompt.blueprint.dynamic_substitution import (
    StringDynamicSubstitution,
)


# auxiliaries  ##################################################################
def _build_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    dynamic_substitution_parser.register_dynamic_substitution_parser(
        subparser
    )
    return root_parser


@pytest.fixture(name="_registry")
def _registry_fixture():
    registry = {
        "some-sub": StringDynamicSubstitution("some text"),
        "other-sub": StringDynamicSubstitution("other text"),
    }
    with patch.object(
        dynamic_substitution_parser, "dynamic_substitution_registry", registry
    ):
        yield registry


# pytest  ######################################################################
class TestRegisterDynamicSubstitutionParser:

    def test_registers_subcommand(_):
        args = _build_parser().parse_args(["dynamic-substitution", "x"])

        assert args.NAME == "x"
        assert (
            args.func is dynamic_substitution_parser._dynamic_substitution_main
        )

    def test_registers_ds_alias(_):
        assert _build_parser().parse_args(["ds", "x"]).NAME == "x"

    def test_bare_command_defaults_to_ls(_):
        assert _build_parser().parse_args(["ds"]).NAME == "ls"


class TestListMode:

    def test_lists_registered_names_sorted(_, _registry, capsys):
        args = _build_parser().parse_args(["dynamic-substitution", "ls"])
        args.func(args)

        assert capsys.readouterr().out.splitlines() == [
            "other-sub",
            "some-sub",
        ]

    def test_bare_command_lists(_, _registry, capsys):
        args = _build_parser().parse_args(["ds"])
        args.func(args)

        assert capsys.readouterr().out.splitlines() == [
            "other-sub",
            "some-sub",
        ]

    def test_lists_nothing_when_registry_empty(_, capsys):
        with patch.object(
            dynamic_substitution_parser, "dynamic_substitution_registry", {}
        ):
            args = _build_parser().parse_args(["ds", "ls"])
            args.func(args)

        assert capsys.readouterr().out == ""

    def test_regex_filters_list(_, _registry, capsys):
        args = _build_parser().parse_args(["ds", "-r", "^some"])
        args.func(args)

        assert capsys.readouterr().out == "some-sub\n"

    def test_json_format(_, _registry, capsys):
        args = _build_parser().parse_args(["ds", "-f", "json"])
        args.func(args)

        assert '"other-sub"' in capsys.readouterr().out


class TestEntryMode:

    def test_prints_content_of_known_entry(_, _registry, capsys):
        args = _build_parser().parse_args(["ds", "some-sub"])
        args.func(args)

        assert capsys.readouterr().out == "some text\n"

    @pytest.mark.parametrize("flag", [["-r", "x"], ["-N"], ["-C"]])
    def test_rejects_list_flags(_, _registry, flag):
        args = _build_parser().parse_args(["ds", "some-sub", *flag])

        with pytest.raises(SystemExit) as info:
            args.func(args)

        assert info.value.code == 1


class TestUnknownName:

    def test_exits_1_and_logs_error_shape(_, _registry, caplog):
        args = _build_parser().parse_args(["ds", "does-not-exist"])

        with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
            with pytest.raises(SystemExit) as info:
                args.func(args)

        assert info.value.code == 1
        assert any(
            rec.levelno == logging.ERROR
            and "unknown dynamic-substitution: does-not-exist" in rec.message
            for rec in caplog.records
        )

    def test_names_the_closest_when_near(_, _registry, caplog):
        args = _build_parser().parse_args(["ds", "some-sbu"])

        with caplog.at_level(logging.ERROR, logger=LOGGER_NAME):
            with pytest.raises(SystemExit):
                args.func(args)

        assert "did you mean: some-sub" in caplog.text
