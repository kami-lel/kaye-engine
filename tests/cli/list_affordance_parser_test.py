"""
list_affordance_parser_test.py

Unit Tests (using pytest) for:

_list_affordance_main, register_list_affordance_parser
"""

from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine.cli import list_affordance_parser


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
    registry = {"some-affordance": object(), "other-affordance": object()}
    with patch.object(list_affordance_parser, "affordance_registry", registry):
        yield registry


# pytest  ######################################################################
class TestRegisterListAffordanceParser:

    def test_registers_list_affordance_subcommand(self):
        parser = _build_list_affordance_parser()
        args = parser.parse_args(["list-affordance"])

        assert args.func is list_affordance_parser._list_affordance_main

    def test_registers_lsa_alias(self):
        parser = _build_list_affordance_parser()
        args = parser.parse_args(["lsa"])

        assert args.func is list_affordance_parser._list_affordance_main


class TestListAffordanceMain:

    def test_lists_registered_affordances_sorted(self, _fake_registry, capsys):
        parser = _build_list_affordance_parser()
        args = parser.parse_args(["list-affordance"])
        args.func(args)

        out = capsys.readouterr().out
        assert out.splitlines() == ["other-affordance", "some-affordance"]

    def test_lists_nothing_when_registry_empty(self, capsys):
        with patch.object(list_affordance_parser, "affordance_registry", {}):
            parser = _build_list_affordance_parser()
            args = parser.parse_args(["list-affordance"])
            args.func(args)

        out = capsys.readouterr().out
        assert out == ""
