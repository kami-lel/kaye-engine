"""
list_view_test.py

Unit Tests (using pytest) for:

add_list_flags, filter_rows, select_columns, print_rows, print_cards,
print_groups
"""

import io
import json
from argparse import ArgumentParser

import pytest

from kaye_engine.cli.list_view import (
    add_list_flags,
    filter_rows,
    print_cards,
    print_groups,
    print_rows,
    select_columns,
)

_COLUMNS = ("remark", "variants")
_ROWS = (
    ("beta", {"remark": "second", "variants": ["x", "y"]}),
    ("alpha", {"remark": "first", "variants": []}),
)


# auxiliaries  #################################################################
class _Tty(io.StringIO):
    def isatty(self):
        return True


def _parse(argv):
    parser = ArgumentParser()
    add_list_flags(parser, _COLUMNS)
    return parser.parse_args(argv)


def _print(argv, rows=_ROWS, columns=None, stream=None):
    args = _parse(argv)
    stream = stream or io.StringIO()
    columns = select_columns(args, _COLUMNS) if columns is None else columns
    print_rows(args, "name", columns, rows, stream=stream)
    return stream.getvalue()


# pytest  ######################################################################
class TestAddListFlags:

    def test_defaults(_):
        args = _parse([])

        assert args.regex == []
        assert args.columns is None
        assert (args.long, args.names_only, args.no_color) == (
            False,
            False,
            False,
        )
        assert args.format is None

    def test_short_and_long_forms_match(_):
        short = _parse(["-l", "-N", "-C", "-f", "json", "-c", "remark"])
        long = _parse(
            [
                "--long",
                "--names-only",
                "--no-color",
                "--format",
                "json",
                "--columns",
                "remark",
            ]
        )

        assert vars(short) == vars(long)

    @pytest.mark.parametrize(
        "old_flag", ["-i", "-I", "-m", "-s", "-v", "--info", "--no-info"]
    )
    def test_rejects_old_flags(_, old_flag):
        with pytest.raises(SystemExit):
            _parse([old_flag])

    def test_rejects_positional_argument(_):
        with pytest.raises(SystemExit):
            _parse(["alpha"])

    def test_rejects_invalid_regex(_, capsys):
        with pytest.raises(SystemExit):
            _parse(["-r", "["])

        assert "invalid regex" in capsys.readouterr().err

    def test_rejects_unknown_column_naming_the_valid_ones(_, capsys):
        with pytest.raises(SystemExit):
            _parse(["-c", "nope"])

        err = capsys.readouterr().err
        assert "unknown column 'nope'" in err
        assert "remark, variants" in err

    def test_rejects_unknown_format(_):
        with pytest.raises(SystemExit):
            _parse(["-f", "xml"])


class TestFilterRows:

    def test_no_pattern_keeps_every_row(_):
        assert filter_rows(_parse([]), _ROWS) == list(_ROWS)

    def test_pattern_searches_not_anchors(_):
        names = [r[0] for r in filter_rows(_parse(["-r", "lph"]), _ROWS)]

        assert names == ["alpha"]

    def test_several_patterns_or_together(_):
        args = _parse(["-r", "^a", "-r", "^b"])

        assert [r[0] for r in filter_rows(args, _ROWS)] == ["beta", "alpha"]


class TestSelectColumns:

    def test_default(_):
        assert select_columns(_parse([]), ["remark"]) == ["remark"]

    def test_given_order_wins(_):
        args = _parse(["-c", "variants,remark"])

        assert select_columns(args, _COLUMNS) == ["variants", "remark"]


class TestPrintRows:

    def test_piped_default_is_tsv_with_full_lists(_):
        assert _print([]) == (
            "name\tremark\tvariants\n"
            "beta\tsecond\tx,y\n"
            "alpha\tfirst\t\n"
        )

    def test_tty_default_is_aligned_table_with_counts(_):
        out = _print(["-C"], stream=_Tty())

        assert out == (
            "NAME   REMARK  VARIANTS\n"
            "beta   second  2\n"
            "alpha  first   0\n"
        )

    def test_names_only_has_no_heading(_):
        assert _print(["-N"]) == "beta\nalpha\n"

    def test_json_keeps_lists_whole(_):
        records = json.loads(_print(["-f", "json"]))

        assert records[0] == {
            "name": "beta",
            "remark": "second",
            "variants": ["x", "y"],
        }

    def test_columns_pick_and_order(_):
        out = _print(["-c", "variants,remark"])

        assert out.splitlines()[0] == "name\tvariants\tremark"

    def test_filter_applies(_):
        assert _print(["-r", "^b", "-N"]) == "beta\n"

    def test_empty_rows_still_print_heading(_):
        assert _print([], rows=()) == "name\tremark\tvariants\n"

    def test_color_on_a_tty_uses_ansi(_):
        assert "\033[" in _print([], stream=_Tty())

    def test_no_color_flag_strips_ansi(_):
        assert "\033[" not in _print(["-C"], stream=_Tty())

    def test_no_color_env_strips_ansi(_, monkeypatch):
        monkeypatch.setenv("NO_COLOR", "1")

        assert "\033[" not in _print([], stream=_Tty())

    def test_empty_no_color_env_is_ignored(_, monkeypatch):
        monkeypatch.setenv("NO_COLOR", "")

        assert "\033[" in _print([], stream=_Tty())

    @pytest.mark.parametrize("fmt", ["tsv", "json"])
    def test_machine_formats_never_color(_, fmt):
        assert "\033[" not in _print(["-f", fmt], stream=_Tty())

    def test_names_only_never_colors(_):
        assert "\033[" not in _print(["-N"], stream=_Tty())

    def test_piped_never_colors(_):
        assert "\033[" not in _print(["-f", "table"])


class TestPrintCards:

    def _cards(_):
        return [
            (
                "code",
                "terminal",
                [
                    ("mode", "NORMAL"),
                    ("variants", "(4)", ["aa", "bb", "cc", "dd"]),
                ],
            )
        ]

    def test_card_layout(self):
        stream = io.StringIO()
        print_cards(_parse([]), self._cards(), stream=stream, width=80)

        assert stream.getvalue() == (
            "code: terminal\n"
            "  mode      NORMAL\n"
            "  variants  (4)\n"
            "    aa   bb   cc   dd\n"
        )

    def test_names_wrap_to_width(self):
        stream = io.StringIO()
        print_cards(_parse([]), self._cards(), stream=stream, width=14)

        assert stream.getvalue().splitlines()[3:] == [
            "    aa   bb",
            "    cc   dd",
        ]

    def test_no_remark_leaves_no_colon(self):
        stream = io.StringIO()
        card = ("code", "", [("mode", "NORMAL")])
        print_cards(_parse([]), [card], stream=stream, width=80)

        assert stream.getvalue().splitlines()[0] == "code"


class TestPrintGroups:

    def test_header_with_count_then_aligned_rows(_):
        stream = io.StringIO()
        groups = [
            ("agent", [("a-long-name", "does a")]),
            ("cli", [("b", "does b"), ("c", "")]),
        ]
        print_groups(_parse([]), groups, stream=stream)

        assert stream.getvalue() == (
            "agent (1)\n"
            "  a-long-name   does a\n"
            "cli (2)\n"
            "  b             does b\n"
            "  c\n"
        )

    def test_color_on_a_tty(_):
        stream = _Tty()
        print_groups(_parse([]), [("agent", [("a", "x")])], stream=stream)

        assert "\033[" in stream.getvalue()
