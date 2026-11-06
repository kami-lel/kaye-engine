"""
list_affordance_parser_test.py

Unit Tests (using pytest) for:

_list_affordance_main, register_list_affordance_parser
"""

from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine.cli import list_affordance_parser
from kaye_engine.prompt.affordance_registry import Affordance


# auxiliaries  ##################################################################
def _build_list_affordance_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    list_affordance_parser.register_list_affordance_parser(subparser)
    return root_parser


@pytest.fixture(autouse=True)
def _no_corpus_setup_guard():
    with patch.object(
        list_affordance_parser, "check_corpus_setup_for_cli", lambda: None
    ):
        yield


@pytest.fixture
def _fake_registry():
    registry = {
        "some-affordance": Affordance(
            canonical_name="some-affordance", remark="do some"
        ),
        "other-affordance": Affordance(canonical_name="other-affordance"),
    }
    with patch.object(list_affordance_parser, "affordance_registry", registry):
        yield registry


# pytest  ######################################################################
class TestRegisterListAffordanceParser:

    def test_registers_affordance_subcommand(self):
        parser = _build_list_affordance_parser()
        args = parser.parse_args(["affordance"])

        assert args.func is list_affordance_parser._list_affordance_main

    def test_rejects_old_names(self):
        parser = _build_list_affordance_parser()

        for old_name in ("list-affordance", "lsa"):
            with pytest.raises(SystemExit):
                parser.parse_args([old_name])

    def test_registers_afd_alias(self):
        parser = _build_list_affordance_parser()
        args = parser.parse_args(["afd"])

        assert args.func is list_affordance_parser._list_affordance_main


def _run(argv):
    parser = _build_list_affordance_parser()
    args = parser.parse_args(argv)
    args.func(args)


class TestListAffordanceMain:

    def test_default_prints_heading_and_sorted_rows(
        self, _fake_registry, capsys
    ):
        _run(["affordance"])

        assert capsys.readouterr().out == (
            "affordance\tremark\n"
            "other-affordance\t\n"
            "some-affordance\tdo some\n"
        )

    def test_info_matches_default(self, _fake_registry, capsys):
        _run(["afd", "-i"])
        with_info = capsys.readouterr().out
        _run(["afd"])

        assert with_info == capsys.readouterr().out

    def test_no_info_prints_names_only_without_heading(
        self, _fake_registry, capsys
    ):
        _run(["afd", "-I"])

        assert capsys.readouterr().out == (
            "other-affordance\nsome-affordance\n"
        )

    def test_long_flag(self, _fake_registry, capsys):
        _run(["afd", "--no-info"])

        assert capsys.readouterr().out == (
            "other-affordance\nsome-affordance\n"
        )

    def test_rejects_old_remark_flags(self, _fake_registry):
        parser = _build_list_affordance_parser()

        for old_flag in ("-r", "-R", "--remark", "--no-remark"):
            with pytest.raises(SystemExit):
                parser.parse_args(["afd", old_flag])

    def test_lists_nothing_when_registry_empty(self, capsys):
        with patch.object(list_affordance_parser, "affordance_registry", {}):
            _run(["affordance", "-I"])

        assert capsys.readouterr().out == ""

    def test_empty_registry_still_prints_heading(self, capsys):
        with patch.object(list_affordance_parser, "affordance_registry", {}):
            _run(["affordance"])

        assert capsys.readouterr().out == "affordance\tremark\n"
