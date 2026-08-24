"""
list_variant_parser_test.py

Unit Tests (using pytest) for:

_list_variant_main, register_list_variant_parser
"""

from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine.cli import list_variant_parser


# auxiliaries  ##################################################################
def _build_list_variant_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    list_variant_parser.register_list_variant_parser(subparser)
    return root_parser


@pytest.fixture(autouse=True)
def _no_corpus_setup_guard():
    with patch.object(
        list_variant_parser, "check_corpus_setup_for_cli", lambda: None
    ):
        yield


@pytest.fixture
def _fake_registry():
    registry = {"some-variant": object(), "other-variant": object()}
    with patch.object(list_variant_parser, "variant_registry", registry):
        yield registry


# pytest  ######################################################################
class TestRegisterListVariantParser:

    def test_registers_list_variant_subcommand(self):
        parser = _build_list_variant_parser()
        args = parser.parse_args(["list-variant"])

        assert args.func is list_variant_parser._list_variant_main

    def test_registers_lsv_alias(self):
        parser = _build_list_variant_parser()
        args = parser.parse_args(["lsv"])

        assert args.func is list_variant_parser._list_variant_main


class TestListVariantMain:

    def test_lists_registered_variants_sorted(self, _fake_registry, capsys):
        parser = _build_list_variant_parser()
        args = parser.parse_args(["list-variant"])
        args.func(args)

        out = capsys.readouterr().out
        assert out.splitlines() == ["other-variant", "some-variant"]

    def test_lists_nothing_when_registry_empty(self, capsys):
        with patch.object(list_variant_parser, "variant_registry", {}):
            parser = _build_list_variant_parser()
            args = parser.parse_args(["list-variant"])
            args.func(args)

        out = capsys.readouterr().out
        assert out == ""
