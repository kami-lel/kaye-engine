"""
list_variant_parser_test.py

Unit Tests (using pytest) for:

_list_variant_main, register_list_variant_parser
"""

from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine.cli import list_variant_parser
from kaye_engine.prompt.affordance_registry import Variant


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
    # names interleave across affordances, so name order differs from group
    # order: b-aff holds `a-var` and `z-var`, a-aff holds `m-var`
    registry = {
        entry.canonical_name: entry
        for entry in (
            Variant(
                canonical_name="a-var", affordance_name="b-aff", remark="do a"
            ),
            Variant(
                canonical_name="m-var", affordance_name="a-aff", remark="do m"
            ),
            Variant(canonical_name="z-var", affordance_name="b-aff"),
        )
    }
    with patch.object(list_variant_parser, "variant_registry", registry):
        yield registry


# pytest  ######################################################################
class TestRegisterListVariantParser:

    def test_registers_variant_subcommand(self):
        parser = _build_list_variant_parser()
        args = parser.parse_args(["variant"])

        assert args.func is list_variant_parser._list_variant_main

    def test_rejects_old_names(self):
        parser = _build_list_variant_parser()

        for old_name in ("list-variant", "lsv"):
            with pytest.raises(SystemExit):
                parser.parse_args([old_name])

    def test_registers_var_alias(self):
        parser = _build_list_variant_parser()
        args = parser.parse_args(["var"])

        assert args.func is list_variant_parser._list_variant_main


def _run(argv):
    parser = _build_list_variant_parser()
    args = parser.parse_args(argv)
    args.func(args)


class TestListVariantMain:

    def test_default_prints_heading_and_3_columns_grouped(
        self, _fake_registry, capsys
    ):
        _run(["variant"])

        assert capsys.readouterr().out == (
            "variant\taffordance\tremark\n"
            "m-var\ta-aff\tdo m\n"
            "a-var\tb-aff\tdo a\n"
            "z-var\tb-aff\t\n"
        )

    def test_info_equals_both_column_flags(self, _fake_registry, capsys):
        _run(["var", "-i"])
        info = capsys.readouterr().out
        _run(["var", "-r", "-a"])

        assert info == capsys.readouterr().out

    def test_no_info_prints_names_grouped_without_heading(
        self, _fake_registry, capsys
    ):
        _run(["var", "-I"])

        assert capsys.readouterr().out == "m-var\na-var\nz-var\n"

    def test_remark_only(self, _fake_registry, capsys):
        _run(["var", "-r"])

        assert capsys.readouterr().out == (
            "variant\tremark\nm-var\tdo m\na-var\tdo a\nz-var\t\n"
        )

    def test_affordance_only(self, _fake_registry, capsys):
        _run(["var", "-a"])

        assert capsys.readouterr().out == (
            "variant\taffordance\n"
            "m-var\ta-aff\n"
            "a-var\tb-aff\n"
            "z-var\tb-aff\n"
        )

    def test_flags_apply_in_order_last_wins(self, _fake_registry, capsys):
        _run(["var", "-I", "-r"])
        remark_only = capsys.readouterr().out
        _run(["var", "-r", "-I"])
        nothing = capsys.readouterr().out

        assert remark_only.splitlines()[0] == "variant\tremark"
        assert nothing == "m-var\na-var\nz-var\n"

    def test_long_flags(self, _fake_registry, capsys):
        _run(["variant", "--no-info", "--affordance"])

        assert capsys.readouterr().out.splitlines()[0] == (
            "variant\taffordance"
        )

    def test_group_order_holds_without_the_affordance_column(
        self, _fake_registry, capsys
    ):
        _run(["var", "-r"])
        _, *rows = capsys.readouterr().out.splitlines()

        assert [row.split("\t")[0] for row in rows] == [
            "m-var",
            "a-var",
            "z-var",
        ]

    def test_lists_nothing_when_registry_empty(self, capsys):
        with patch.object(list_variant_parser, "variant_registry", {}):
            _run(["variant", "-I"])

        assert capsys.readouterr().out == ""

    def test_empty_registry_still_prints_heading(self, capsys):
        with patch.object(list_variant_parser, "variant_registry", {}):
            _run(["variant"])

        assert capsys.readouterr().out == "variant\taffordance\tremark\n"
