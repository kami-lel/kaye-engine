"""
list_view_test.py

Unit Tests (using pytest) for:

add_list_flags, add_name_list_flags, track_given_flags,
reject_given_flags, filter_rows, select_columns, print_rows, print_cards,
print_groups, print_banner, print_section, print_names, is_human_view
"""

import io
import json
from argparse import ArgumentParser

import pytest

from kaye_engine.cli.list_view import (
    add_list_flags,
    add_name_list_flags,
    filter_rows,
    is_human_view,
    make_renderer,
    print_banner,
    print_cards,
    print_groups,
    print_names,
    print_rows,
    print_section,
    reject_given_flags,
    select_columns,
    track_given_flags,
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

    def test_tty_default_is_aligned_table_with_joined_lists(_):
        out = _print(["-C"], stream=_Tty())

        assert out == (
            "name   remark  variants\n"
            "beta   second  x,y\n"
            "alpha  first\n"
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
            "    aa  bb  cc  dd\n"
        )

    def test_names_wrap_to_width(self):
        stream = io.StringIO()
        print_cards(_parse([]), self._cards(), stream=stream, width=14)

        assert stream.getvalue().splitlines()[3:] == [
            "    aa  bb",
            "    cc  dd",
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
            "  a-long-name  does a\n"
            "cli (2)\n"
            "  b            does b\n"
            "  c\n"
        )

    def test_color_on_a_tty(_):
        stream = _Tty()
        print_groups(_parse([]), [("agent", [("a", "x")])], stream=stream)

        assert "\033[" in stream.getvalue()


class TestHumanView:

    def test_tty_is_human(_):
        assert is_human_view(_Tty())

    def test_pipe_is_not_human(_):
        assert not is_human_view(io.StringIO())


class TestPrintBanner:

    def test_plain_banner_is_80_wide_centered_cb5(_):
        stream = io.StringIO()
        print_banner(_parse([]), "title", stream)

        line = stream.getvalue().rstrip("\n")
        assert len(line) == 80
        assert "  title  " in line
        assert set(line.replace("  title  ", "")) == {"-"}

    def test_tty_colors_ruler(_, monkeypatch):
        monkeypatch.delenv("NO_COLOR", raising=False)
        stream = _Tty()
        print_banner(_parse([]), "title", stream)

        assert "\033[" in stream.getvalue()

    def test_no_color_flag_keeps_banner_plain(_):
        stream = _Tty()
        print_banner(_parse(["-C"]), "title", stream)

        assert "\033[" not in stream.getvalue()
        assert "  title  " in stream.getvalue()

    def test_no_color_env_keeps_banner_plain(_, monkeypatch):
        monkeypatch.setenv("NO_COLOR", "1")
        stream = _Tty()
        print_banner(_parse([]), "title", stream)

        assert "\033[" not in stream.getvalue()

    def test_args_without_list_flags_are_accepted(_):
        stream = io.StringIO()
        print_banner(object(), "title", stream)

        assert "  title  " in stream.getvalue()


class TestPrintSection:

    def test_banner_over_lines(_):
        stream = io.StringIO()
        print_section(_parse([]), "head", ["a", "b"], stream)

        lines = stream.getvalue().splitlines()
        assert "  head  " in lines[0]
        assert lines[1:] == ["a", "b"]

    def test_names_get_name_color_on_tty(_, monkeypatch):
        monkeypatch.delenv("NO_COLOR", raising=False)
        stream = _Tty()
        print_section(_parse([]), "head", ["a"], stream, is_names=True)

        assert "\033[96ma\033[0m" in stream.getvalue()


class TestPrintNames:

    def test_piped_is_bare_names(_):
        stream = io.StringIO()
        print_names(_parse([]), "things", ["b", "a"], stream)

        assert stream.getvalue() == "b\na\n"

    def test_tty_has_banner_with_count_and_colored_names(_, monkeypatch):
        monkeypatch.delenv("NO_COLOR", raising=False)
        stream = _Tty()
        print_names(_parse([]), "things", ["a", "b"], stream)

        out = stream.getvalue()
        assert "  things (2)  " in out
        assert "\033[96ma\033[0m" in out

    def test_tty_no_color_is_banner_and_plain_names(_):
        stream = _Tty()
        print_names(_parse(["-C"]), "things", ["a"], stream)

        lines = stream.getvalue().splitlines()
        assert "  things (1)  " in lines[0]
        assert lines[1:] == ["a"]


def _parse_names(argv):
    parser = ArgumentParser()
    add_name_list_flags(parser)
    return parser.parse_args(argv)


class TestPrintNamesFlags:

    def test_regex_filters_names(_):
        stream = io.StringIO()
        print_names(
            _parse_names(["-r", "^a"]), "things", ["ab", "b", "ac"], stream
        )

        assert stream.getvalue() == "ab\nac\n"

    def test_names_only_on_tty_has_no_banner(_):
        stream = _Tty()
        print_names(_parse_names(["-N"]), "things", ["a", "b"], stream)

        assert stream.getvalue() == "a\nb\n"

    def test_json_is_array_of_names(_):
        stream = io.StringIO()
        print_names(_parse_names(["-f", "json"]), "things", ["a"], stream)

        assert json.loads(stream.getvalue()) == ["a"]

    def test_table_forced_on_pipe_has_banner(_):
        stream = io.StringIO()
        print_names(_parse_names(["-f", "table"]), "things", ["a"], stream)

        lines = stream.getvalue().splitlines()
        assert "  things (1)  " in lines[0]
        assert lines[1:] == ["a"]

    def test_tsv_on_tty_is_bare(_):
        stream = _Tty()
        print_names(_parse_names(["-f", "tsv"]), "things", ["a"], stream)

        assert stream.getvalue() == "a\n"


class TestNoMatchWarning:

    def test_names_filter_that_keeps_nothing_warns(_, caplog):
        with caplog.at_level("WARNING"):
            print_names(
                _parse_names(["-r", "zz", "-r", "yy"]),
                "things",
                ["a"],
                io.StringIO(),
            )

        assert "no things match zz or yy" in caplog.text

    def test_rows_filter_that_keeps_nothing_warns(_, caplog):
        with caplog.at_level("WARNING"):
            _print(["-r", "zz"], stream=io.StringIO())

        assert "no" in caplog.text and "match zz" in caplog.text

    def test_no_pattern_stays_quiet(_, caplog):
        with caplog.at_level("WARNING"):
            print_names(_parse_names([]), "things", [], io.StringIO())

        assert caplog.text == ""


class TestGivenFlags:

    @staticmethod
    def _build():
        parser = ArgumentParser()
        parser.add_argument("-s", "--sparseness", type=int, default=0)
        parser.add_argument("--flag", action="store_true")
        track_given_flags(parser, ["sparseness", "flag"])
        return parser

    def test_default_value_is_not_given(_):
        args = TestGivenFlags._build().parse_args([])

        reject_given_flags(args, ["sparseness"], "list mode")

    def test_flag_given_with_its_default_value_is_rejected(_):
        args = TestGivenFlags._build().parse_args(["-s", "0"])

        with pytest.raises(SystemExit) as info:
            reject_given_flags(args, ["sparseness"], "list mode")

        assert info.value.code == 1

    def test_message_names_long_flag_and_mode(_, caplog):
        args = TestGivenFlags._build().parse_args(["-s", "2"])

        with pytest.raises(SystemExit):
            reject_given_flags(args, ["sparseness"], "list mode")

        assert "--sparseness does not apply in list mode" in caplog.text

    def test_flag_outside_dests_is_ignored(_):
        args = TestGivenFlags._build().parse_args(["--flag"])

        reject_given_flags(args, ["sparseness"], "list mode")


class TestMakeRenderer:

    def test_tty_gets_renderer(_, monkeypatch):
        monkeypatch.delenv("NO_COLOR", raising=False)

        assert make_renderer(_parse([]), _Tty()) is not None

    def test_pipe_gets_none(_):
        assert make_renderer(_parse([]), io.StringIO()) is None

    def test_no_color_flag_gets_none(_):
        assert make_renderer(_parse(["-C"]), _Tty()) is None

    def test_no_color_env_gets_none(_, monkeypatch):
        monkeypatch.setenv("NO_COLOR", "1")

        assert make_renderer(_parse([]), _Tty()) is None


class TestHeading:

    def _cards(_):
        return [("t1", "r", []), ("t2", "r", [])]

    def _groups(_):
        return [("g", [("a", "x"), ("b", "y")]), ("h", [("c", "z")])]

    def test_rows_tty_table_has_banner_with_count(_):
        stream = _Tty()
        print_rows(
            _parse([]), "name", ["remark"], _ROWS, stream, heading="things"
        )
        assert "  things (2)  " in stream.getvalue()

    def test_rows_filtered_count(_):
        stream = _Tty()
        print_rows(
            _parse(["-r", "^a"]),
            "name",
            ["remark"],
            _ROWS,
            stream,
            heading="things",
        )

        assert "  things (1)  " in stream.getvalue()

    @pytest.mark.parametrize("argv", [["-f", "tsv"], ["-f", "json"], ["-N"]])
    def test_rows_machine_formats_have_no_banner(_, argv):
        stream = _Tty()
        print_rows(
            _parse(argv), "name", ["remark"], _ROWS, stream, heading="things"
        )

        assert "things" not in stream.getvalue()

    def test_rows_piped_has_no_banner(_):
        stream = io.StringIO()
        print_rows(
            _parse(["-f", "table"]),
            "name",
            ["remark"],
            _ROWS,
            stream,
            heading="things",
        )

        assert "things" not in stream.getvalue()

    def test_cards_tty_banner_counts_cards(_):
        stream = _Tty()
        print_cards(_parse([]), _._cards(), stream, heading="cards")

        assert "  cards (2)  " in stream.getvalue()

    def test_cards_piped_has_no_banner(_):
        stream = io.StringIO()
        print_cards(_parse([]), _._cards(), stream, heading="cards")

        assert "cards" not in stream.getvalue()

    def test_groups_tty_banner_counts_all_rows(_):
        stream = _Tty()
        print_groups(_parse([]), _._groups(), stream, heading="groups")

        assert "  groups (3)  " in stream.getvalue()

    def test_groups_piped_has_no_banner(_):
        stream = io.StringIO()
        print_groups(_parse([]), _._groups(), stream, heading="groups")

        assert "groups" not in stream.getvalue()
