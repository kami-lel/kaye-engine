"""
affordance_parser_test.py

Unit Tests (using pytest) for:

_affordance_main, register_affordance_parser
"""

from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine.cli import affordance_parser


# auxiliaries  ##################################################################
def _build_affordance_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    affordance_parser.register_affordance_parser(subparser)
    return root_parser


@pytest.fixture(autouse=True)
def _no_corpus_setup_guard():
    with patch.object(
        affordance_parser, "check_corpus_setup_for_cli", lambda: None
    ):
        yield


@pytest.fixture
def _fake_registry():
    registry = {"some-affordance": object(), "other-affordance": object()}
    with patch.object(affordance_parser, "affordance_registry", registry):
        yield registry


# pytest  ######################################################################
class TestRegisterAffordanceParser:

    def test_registers_affordance_subcommand(self):
        parser = _build_affordance_parser()
        args = parser.parse_args(["affordance"])

        assert args.func is affordance_parser._affordance_main


class TestAffordanceMain:

    def test_lists_registered_affordances_sorted(self, _fake_registry, capsys):
        parser = _build_affordance_parser()
        args = parser.parse_args(["affordance"])
        args.func(args)

        out = capsys.readouterr().out
        assert out.splitlines() == ["other-affordance", "some-affordance"]

    def test_lists_nothing_when_registry_empty(self, capsys):
        with patch.object(affordance_parser, "affordance_registry", {}):
            parser = _build_affordance_parser()
            args = parser.parse_args(["affordance"])
            args.func(args)

        out = capsys.readouterr().out
        assert out == ""
