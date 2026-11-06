"""
list_variant_parser_test.py

Unit Tests (using pytest) for:

_list_variant_main, register_list_variant_parser
"""

import json
from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.cli import list_variant_parser
from kaye_engine.prompt.affordance_registry import Variant

_HEADING = "variant\taffordance\tremark"


# auxiliaries  #################################################################
def _build_list_variant_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    list_variant_parser.register_list_variant_parser(subparser)
    return root_parser


def _run(argv):
    parser = _build_list_variant_parser()
    args = parser.parse_args(argv)
    args.func(args)


@pytest.fixture(autouse=True)
def _fixed_width(monkeypatch):
    monkeypatch.setenv("COLUMNS", "80")


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

    @pytest.mark.parametrize(
        "old_flag", ["-i", "-I", "-R", "--info", "--no-info", "--remark"]
    )
    def test_rejects_old_flags(self, old_flag):
        parser = _build_list_variant_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["var", old_flag])

    def test_rejects_positional_argument(self):
        parser = _build_list_variant_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["var", "cli"])

    def test_rejects_invalid_affordance_regex(self):
        parser = _build_list_variant_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["var", "-a", "["])


@pytest.mark.usefixtures("_fake_registry")
class TestListVariantMain:

    def test_piped_default_is_flat_tsv_sorted_by_affordance_then_name(
        self, capsys
    ):
        _run(["variant"])

        assert capsys.readouterr().out == (
            _HEADING + "\n"
            "m-var\ta-aff\tdo m\n"
            "a-var\tb-aff\tdo a\n"
            "z-var\tb-aff\t\n"
        )

    def test_table_groups_under_affordance_headers_with_counts(self, capsys):
        _run(["var", "-f", "table"])

        assert capsys.readouterr().out == (
            "a-aff (1)\n"
            "  m-var   do m\n"
            "b-aff (2)\n"
            "  a-var   do a\n"
            "  z-var\n"
        )

    def test_flat_prints_an_affordance_column(self, capsys):
        _run(["var", "-f", "table", "-F"])

        assert capsys.readouterr().out == (
            "VARIANT  AFFORDANCE  REMARK\n"
            "m-var    a-aff       do m\n"
            "a-var    b-aff       do a\n"
            "z-var    b-aff\n"
        )

    def test_long_flag_for_flat(self, capsys):
        _run(["var", "-f", "table", "--flat"])

        assert capsys.readouterr().out.startswith("VARIANT  AFFORDANCE")

    def test_columns_imply_a_flat_table(self, capsys):
        _run(["var", "-f", "table", "-c", "remark"])

        assert capsys.readouterr().out == (
            "VARIANT  REMARK\nm-var    do m\na-var    do a\nz-var\n"
        )

    def test_columns_pick_and_order_in_tsv(self, capsys):
        _run(["var", "-c", "remark,affordance"])

        assert capsys.readouterr().out.splitlines()[0] == (
            "variant\tremark\taffordance"
        )

    def test_unknown_column_is_rejected(self):
        parser = _build_list_variant_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["var", "-c", "nope"])

    def test_names_only_keeps_group_order(self, capsys):
        _run(["var", "-N"])

        assert capsys.readouterr().out == "m-var\na-var\nz-var\n"

    def test_affordance_filter(self, capsys):
        _run(["var", "-a", "^b-", "-N"])

        assert capsys.readouterr().out == "a-var\nz-var\n"

    def test_affordance_filters_or_together(self, capsys):
        _run(["var", "--affordance", "^a-", "--affordance", "^b-", "-N"])

        assert capsys.readouterr().out == "m-var\na-var\nz-var\n"

    def test_regex_filters_variant_names(self, capsys):
        _run(["var", "-r", "^[am]-", "-N"])

        assert capsys.readouterr().out == "m-var\na-var\n"

    def test_regex_and_affordance_filters_both_apply(self, capsys):
        _run(["var", "-r", "^z", "-a", "^b-", "-N"])
        both = capsys.readouterr().out
        _run(["var", "-r", "^z", "-a", "^a-", "-N"])
        disjoint = capsys.readouterr().out

        assert both == "z-var\n"
        assert disjoint == ""

    def test_grouped_table_filters_empty_groups_away(self, capsys):
        _run(["var", "-f", "table", "-a", "^a-"])

        assert capsys.readouterr().out == "a-aff (1)\n  m-var   do m\n"

    def test_json(self, capsys):
        _run(["var", "-f", "json", "-r", "^a-var$"])

        assert json.loads(capsys.readouterr().out) == [
            {"variant": "a-var", "affordance": "b-aff", "remark": "do a"}
        ]

    def test_long_prints_a_card_with_sidecar_names(self, capsys):
        _run(["var", "-l", "-r", "^a-var$"])

        assert capsys.readouterr().out == (
            "a-var: do a\n"
            "  affordance     b-aff\n"
            "  usage sidecar  [a-var] Usage\n"
            "  lack sidecar   [a-var] Lack\n"
        )

    def test_names_only_beats_long(self, capsys):
        _run(["var", "-l", "-N"])

        assert capsys.readouterr().out == "m-var\na-var\nz-var\n"

    def test_json_beats_long(self, capsys):
        _run(["var", "-l", "-f", "json"])

        assert len(json.loads(capsys.readouterr().out)) == 3

    def test_populated_registry_logs_no_note(self, caplog):
        with caplog.at_level(1, logger=LOGGER_NAME):
            _run(["var"])

        assert not caplog.records


class TestEmptyRegistry:

    def test_names_only_prints_nothing(self, capsys):
        with patch.object(list_variant_parser, "variant_registry", {}):
            _run(["variant", "-N"])

        assert capsys.readouterr().out == ""

    def test_still_prints_heading(self, capsys):
        with patch.object(list_variant_parser, "variant_registry", {}):
            _run(["variant"])

        assert capsys.readouterr().out == _HEADING + "\n"

    def test_grouped_table_prints_nothing(self, capsys):
        with patch.object(list_variant_parser, "variant_registry", {}):
            _run(["variant", "-f", "table"])

        assert capsys.readouterr().out == ""

    def test_logs_one_note_and_no_error(self, caplog):
        with patch.object(list_variant_parser, "variant_registry", {}):
            with caplog.at_level(1, logger=LOGGER_NAME):
                _run(["variant"])

        assert len(caplog.records) == 1
        assert "no variants registered" in caplog.records[0].message
        assert caplog.records[0].levelname == "NOTE"
