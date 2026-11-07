"""
list_affordance_parser_test.py

Unit Tests (using pytest) for:

_list_affordance_main, register_list_affordance_parser
"""

import json
from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.cli import list_affordance_parser
from kaye_engine.prompt.affordance_registry import Affordance, Variant

_HEADING = "affordance\tvariants\tremark"


# auxiliaries  #################################################################
def _build_list_affordance_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    list_affordance_parser.register_list_affordance_parser(subparser)
    return root_parser


@pytest.fixture(autouse=True)
def _fixed_width(monkeypatch):
    monkeypatch.setenv("COLUMNS", "80")


@pytest.fixture
def _fake_registry():
    affordances = {
        "some-affordance": Affordance(
            canonical_name="some-affordance", remark="do some"
        ),
        "other-affordance": Affordance(canonical_name="other-affordance"),
    }
    variants = {
        "v-b": Variant(
            canonical_name="v-b",
            affordance_name="some-affordance",
            remark="second",
        ),
        "v-a": Variant(
            canonical_name="v-a",
            affordance_name="some-affordance",
            remark="first",
        ),
    }
    with patch.object(
        list_affordance_parser, "affordance_registry", affordances
    ), patch.object(list_affordance_parser, "variant_registry", variants):
        yield affordances


def _run(argv):
    parser = _build_list_affordance_parser()
    args = parser.parse_args(argv)
    args.func(args)


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

    @pytest.mark.parametrize(
        "old_flag", ["-i", "-I", "-R", "--info", "--no-info", "--no-remark"]
    )
    def test_rejects_old_flags(self, old_flag):
        parser = _build_list_affordance_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["afd", old_flag])

    def test_rejects_positional_argument(self):
        parser = _build_list_affordance_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["afd", "cli"])


@pytest.mark.usefixtures("_fake_registry")
class TestListAffordanceMain:

    def test_default_prints_heading_variants_and_remark(self, capsys):
        _run(["affordance"])

        assert capsys.readouterr().out == (
            _HEADING + "\n"
            "other-affordance\t\t\n"
            "some-affordance\tv-a,v-b\tdo some\n"
        )

    def test_names_only(self, capsys):
        _run(["afd", "-N"])

        assert capsys.readouterr().out == "other-affordance\nsome-affordance\n"

    def test_long_names_only_flag(self, capsys):
        _run(["afd", "--names-only"])

        assert capsys.readouterr().out == "other-affordance\nsome-affordance\n"

    def test_columns_pick_and_order(self, capsys):
        _run(["afd", "-c", "remark,variants"])

        assert capsys.readouterr().out == (
            "affordance\tremark\tvariants\n"
            "other-affordance\t\t\n"
            "some-affordance\tdo some\tv-a,v-b\n"
        )

    def test_unknown_column_is_rejected(self):
        parser = _build_list_affordance_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["afd", "-c", "nope"])

    def test_regex_filters_names(self, capsys):
        _run(["afd", "-r", "^some", "-N"])

        assert capsys.readouterr().out == "some-affordance\n"

    def test_json_lists_variants_whole(self, capsys):
        _run(["afd", "-f", "json", "-r", "^some"])

        assert json.loads(capsys.readouterr().out) == [
            {
                "affordance": "some-affordance",
                "variants": ["v-a", "v-b"],
                "remark": "do some",
            }
        ]

    def test_long_prints_variants_with_remarks_beneath(self, capsys):
        _run(["afd", "-l"])

        assert capsys.readouterr().out == (
            "other-affordance\n"
            "some-affordance: do some\n"
            "  v-a  first\n"
            "  v-b  second\n"
        )

    def test_long_filters_by_regex(self, capsys):
        _run(["afd", "--long", "-r", "^some"])

        assert capsys.readouterr().out.startswith("some-affordance: do some")

    def test_names_only_beats_long(self, capsys):
        _run(["afd", "-l", "-N"])

        assert capsys.readouterr().out == "other-affordance\nsome-affordance\n"

    def test_json_beats_long(self, capsys):
        _run(["afd", "-l", "-f", "json"])

        assert len(json.loads(capsys.readouterr().out)) == 2

    def test_populated_registry_logs_no_note(self, caplog):
        with caplog.at_level(1, logger=LOGGER_NAME):
            _run(["afd"])

        assert not caplog.records


class TestEmptyRegistry:

    def test_lists_nothing_with_names_only(self, capsys):
        with patch.object(list_affordance_parser, "affordance_registry", {}):
            _run(["affordance", "-N"])

        assert capsys.readouterr().out == ""

    def test_still_prints_heading(self, capsys):
        with patch.object(list_affordance_parser, "affordance_registry", {}):
            _run(["affordance"])

        assert capsys.readouterr().out == _HEADING + "\n"

    def test_logs_one_note_and_no_error(self, caplog):
        with patch.object(list_affordance_parser, "affordance_registry", {}):
            with caplog.at_level(1, logger=LOGGER_NAME):
                _run(["affordance"])

        assert len(caplog.records) == 1
        assert "no affordances registered" in caplog.records[0].message
        assert caplog.records[0].levelname == "NOTE"
