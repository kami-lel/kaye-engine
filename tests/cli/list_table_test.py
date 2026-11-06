"""
list_table_test.py

Unit Tests (using pytest) for:

add_info_flags, select_info_columns, print_table
"""

from argparse import ArgumentParser

import pytest

from kaye_engine.cli.list_table import (
    add_info_flags,
    print_table,
    select_info_columns,
)

_COLUMNS = {
    "affordance": ("-a", "--affordance"),
    "remark": ("-r", "--remark"),
}


# auxiliaries  #################################################################
def _selected(argv, columns=None):
    columns = _COLUMNS if columns is None else columns
    parser = ArgumentParser()
    add_info_flags(parser, columns)
    return select_info_columns(parser.parse_args(argv), columns)


# pytest  ######################################################################
class TestSelectInfoColumns:

    def test_no_flag_selects_every_column(_):
        assert _selected([]) == ["affordance", "remark"]

    def test_info_selects_every_column(_):
        assert _selected(["-i"]) == ["affordance", "remark"]

    def test_info_equals_both_column_flags(_):
        assert _selected(["-i"]) == _selected(["-r", "-a"])

    def test_no_info_selects_nothing(_):
        assert _selected(["-I"]) == []

    def test_one_column_flag_selects_only_its_column(_):
        assert _selected(["-r"]) == ["remark"]
        assert _selected(["-a"]) == ["affordance"]

    def test_selection_keeps_column_order_not_flag_order(_):
        assert _selected(["-r", "-a"]) == ["affordance", "remark"]

    def test_no_info_then_column_flag_keeps_only_that_column(_):
        assert _selected(["-I", "-r"]) == ["remark"]

    def test_column_flag_then_no_info_selects_nothing(_):
        assert _selected(["-r", "-I"]) == []

    def test_no_info_then_info_selects_every_column(_):
        assert _selected(["-I", "-i"]) == ["affordance", "remark"]

    def test_long_flags(_):
        assert _selected(["--no-info", "--remark"]) == ["remark"]
        assert _selected(["--info"]) == ["affordance", "remark"]

    def test_column_without_flag_follows_info_and_no_info(_):
        columns = {"remark": None}

        assert _selected([], columns) == ["remark"]
        assert _selected(["-i"], columns) == ["remark"]
        assert _selected(["-I"], columns) == []

    def test_column_without_flag_adds_no_option(_):
        parser = ArgumentParser()
        add_info_flags(parser, {"remark": None})

        with pytest.raises(SystemExit):
            parser.parse_args(["-r"])


class TestPrintTable:

    def test_heading_then_rows(_, capsys):
        rows = [
            ("a", {"affordance": "x", "remark": "do a"}),
            ("b", {"affordance": "y", "remark": ""}),
        ]

        print_table("variant", ["affordance", "remark"], rows)

        assert capsys.readouterr().out == (
            "variant\taffordance\tremark\na\tx\tdo a\nb\ty\t\n"
        )

    def test_only_selected_columns_print(_, capsys):
        rows = [("a", {"affordance": "x", "remark": "do a"})]

        print_table("variant", ["remark"], rows)

        assert capsys.readouterr().out == "variant\tremark\na\tdo a\n"

    def test_no_info_prints_names_without_heading(_, capsys):
        rows = [("a", {"affordance": "x"}), ("b", {"affordance": "y"})]

        print_table("variant", [], rows)

        assert capsys.readouterr().out == "a\nb\n"

    def test_empty_rows_still_print_the_heading(_, capsys):
        print_table("variant", ["remark"], [])

        assert capsys.readouterr().out == "variant\tremark\n"

    def test_empty_rows_without_info_print_nothing(_, capsys):
        print_table("variant", [], [])

        assert capsys.readouterr().out == ""
