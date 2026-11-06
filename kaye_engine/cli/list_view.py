"""
list_view.py

define ``add_list_flags``, ``filter_rows``, ``select_columns``,
``print_rows``, ``print_cards``, ``print_groups``, ``parse_regex`` and
``resolve_format`` -- the shared
mechanism of the list commands (``affordance``, ``variant``,
``render-profile``): one flag set, one name filter, and table, tsv, json,
card and grouped views, colored only through kamilog
"""

import json
import os
import re
import shutil
import sys
from argparse import ArgumentTypeError

from kamilog import AnsiRenderer, AnsiStyle

__all__ = (
    "FMT_JSON",
    "FMT_TABLE",
    "FMT_TSV",
    "add_list_flags",
    "filter_rows",
    "parse_regex",
    "print_cards",
    "print_groups",
    "print_rows",
    "resolve_format",
    "select_columns",
)

# constants  ###################################################################
FMT_TABLE = "table"
FMT_TSV = "tsv"
FMT_JSON = "json"
_FORMATS = (FMT_TABLE, FMT_TSV, FMT_JSON)

_COL_GAP = "  "
_INDENT = "  "
_NAME_GAP = "   "
_DFT_WIDTH = 80

# color roles; every hue comes from kamilog's AnsiStyle
_STYLE_HEAD = AnsiStyle.BOLD
_STYLE_NAME = AnsiStyle.BRIGHT_CYAN
_STYLE_GROUP = AnsiStyle.BOLD | AnsiStyle.BRIGHT_BLUE


# auxiliaries  #################################################################
def parse_regex(text):
    """
    :return: the compiled pattern; used as an argparse ``type``
    :rtype: re.Pattern
    :raises argparse.ArgumentTypeError: ``text`` is not a valid regex
    """
    try:
        return re.compile(text)
    except re.error as err:
        raise ArgumentTypeError(
            "invalid regex {!r}: {}".format(text, err)
        ) from err


def _build_columns_parser(valid):
    """
    :param valid: column names a command offers
    :type valid: tuple[str]
    :return: an argparse ``type`` turning ``a,b`` into ``["a", "b"]``,
            rejecting any name outside ``valid``
    :rtype: collections.abc.Callable
    """

    def parse_columns(text):
        names = [name.strip() for name in text.split(",") if name.strip()]
        if not names:
            raise ArgumentTypeError("no column given")
        for name in names:
            if name not in valid:
                raise ArgumentTypeError(
                    "unknown column {!r}; valid: {}".format(
                        name, ", ".join(valid)
                    )
                )
        return names

    return parse_columns


def _is_color_off(args, fmt):
    """
    :return: if color must stay off whatever the stream: ``-C``,
            ``NO_COLOR`` set and non-empty, a non-table format, or
            names only
    :rtype: bool
    """
    return bool(
        args.no_color
        or os.environ.get("NO_COLOR")
        or fmt != FMT_TABLE
        or args.names_only
    )


def resolve_format(args, stream):
    """
    :return: ``-f`` when given; otherwise table on a TTY, tsv off one
    :rtype: str
    """
    if args.format:
        return args.format
    return FMT_TABLE if stream.isatty() else FMT_TSV


def _build_renderer(args, stream, fmt):
    """
    :return: the run's one kamilog renderer; it also turns itself off
            when ``stream`` is no TTY
    :rtype: kamilog.AnsiRenderer
    """
    return AnsiRenderer(stream, is_disabled=_is_color_off(args, fmt))


def _format_cell(val, fmt):
    """
    :return: ``val`` as cell text; a list is its count in a table, comma-joined
            elsewhere
    :rtype: str
    """
    if isinstance(val, (list, tuple)):
        return str(len(val)) if fmt == FMT_TABLE else ",".join(val)
    return str(val)


def _get_width(width):
    """
    :return: ``width`` when given; otherwise the terminal's
    :rtype: int
    """
    if width:
        return width
    return shutil.get_terminal_size((_DFT_WIDTH, 24)).columns


def _print_tsv(stream, name_heading, columns, rows):
    print("\t".join([name_heading, *columns]), file=stream)
    for name, cells in rows:
        cols = (_format_cell(cells[key], FMT_TSV) for key in columns)
        print("\t".join([name, *cols]), file=stream)


def _print_json(stream, name_heading, columns, rows):
    records = [
        {
            name_heading: name,
            **{key: cells[key] for key in columns},
        }
        for name, cells in rows
    ]
    print(json.dumps(records, indent=2, ensure_ascii=False), file=stream)


def _print_table(stream, renderer, name_heading, columns, rows):
    heads = [name_heading.upper(), *(key.upper() for key in columns)]
    body = [
        [name, *(_format_cell(cells[key], FMT_TABLE) for key in columns)]
        for name, cells in rows
    ]
    widths = [
        max(len(line[i]) for line in [heads, *body]) for i in range(len(heads))
    ]
    last = len(heads) - 1

    def join_line(line, style_of):
        cells = []
        for i, text in enumerate(line):
            padded = text if i == last else text.ljust(widths[i])
            cells.append(style_of(i, padded))
        return _COL_GAP.join(cells).rstrip()

    print(
        join_line(heads, lambda _, text: renderer.color(text, _STYLE_HEAD)),
        file=stream,
    )
    for line in body:
        styled = join_line(
            line, lambda i, text: _style_body_cell(renderer, i, text)
        )
        print(styled, file=stream)


def _style_body_cell(renderer, idx, text):
    """
    :return: ``text`` in the name color for column 0, grey otherwise
    :rtype: str
    """
    if idx == 0:
        return renderer.color(text, _STYLE_NAME)
    return renderer.color_grey(text)


def _layout_names(names, width, indent):
    """
    :return: ``names`` laid out row-major in even columns that fit ``width``
    :rtype: list[str]
    """
    if not names:
        return []

    col_width = max(len(name) for name in names) + len(_NAME_GAP)
    n_cols = max(1, (width - indent) // col_width)
    lines = []
    for start in range(0, len(names), n_cols):
        chunk = names[start : start + n_cols]
        line = "".join(name.ljust(col_width) for name in chunk).rstrip()
        lines.append(" " * indent + line)
    return lines


# Public API  ##################################################################
def add_list_flags(parser, columns):
    """
    add the shared list flags to ``parser``: ``-r/--regex``,
    ``-c/--columns``, ``-l/--long``, ``-N/--names-only``, ``-f/--format``
    and ``-C/--no-color``


    :param parser: the list command's parser
    :type parser: argparse.ArgumentParser
    :param columns: column names the command offers to ``-c``, name column
            excluded
    :type columns: tuple[str]
    """
    parser.add_argument(
        "-r",
        "--regex",
        action="append",
        default=[],
        type=parse_regex,
        metavar="PATTERN",
        help="only names matching PATTERN (regex search); repeat to match "
        "any of several",
    )
    parser.add_argument(
        "-c",
        "--columns",
        type=_build_columns_parser(tuple(columns)),
        metavar="COLS",
        help="comma-separated columns to show, one or more of: "
        + ", ".join(columns),
    )
    parser.add_argument(
        "-l",
        "--long",
        action="store_true",
        help="detail view: one card per row, long lists in full",
    )
    parser.add_argument(
        "-N",
        "--names-only",
        action="store_true",
        help="names only, one per line, no heading",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=_FORMATS,
        help="table (default on a TTY), tsv (default when piped) or json",
    )
    parser.add_argument(
        "-C",
        "--no-color",
        action="store_true",
        help="plain output; NO_COLOR does the same",
    )


def filter_rows(args, rows):
    """
    keep the rows whose name matches any ``-r`` pattern


    :param args: parsed arguments that ran ``add_list_flags``
    :type args: argparse.Namespace
    :param rows: each row is ``(name, payload)``
    :type rows: collections.abc.Iterable[tuple]
    :return: the kept rows, in order; every row when no pattern was given
    :rtype: list[tuple]
    """
    patterns = args.regex
    return [
        row
        for row in rows
        if not patterns or any(pat.search(row[0]) for pat in patterns)
    ]


def select_columns(args, dft_columns):
    """
    :param args: parsed arguments that ran ``add_list_flags``
    :type args: argparse.Namespace
    :param dft_columns: the command's default columns, name column excluded
    :type dft_columns: collections.abc.Iterable[str]
    :return: the ``-c`` columns in the order given; otherwise the default
    :rtype: list[str]
    """
    return list(args.columns) if args.columns else list(dft_columns)


def print_rows(args, name_heading, columns, rows, stream=None):
    """
    print filtered ``rows`` in the chosen format: names only, json, tsv,
    or an aligned colored table


    :param args: parsed arguments that ran ``add_list_flags``
    :type args: argparse.Namespace
    :param name_heading: heading and json key of the name column
    :type name_heading: str
    :param columns: info column keys to print, in order
    :type columns: list[str]
    :param rows: each row is ``(name, {column key: value})``; a list value
            prints as its count in a table, comma-joined in tsv, as is in json
    :type rows: collections.abc.Iterable[tuple]
    :param stream: output stream; default ``sys.stdout``
    :type stream: IO or None
    """
    stream = stream or sys.stdout
    fmt = resolve_format(args, stream)
    rows = filter_rows(args, rows)

    if args.names_only:
        for name, _ in rows:
            print(name, file=stream)
    elif fmt == FMT_JSON:
        _print_json(stream, name_heading, columns, rows)
    elif fmt == FMT_TSV:
        _print_tsv(stream, name_heading, columns, rows)
    else:
        renderer = _build_renderer(args, stream, fmt)
        _print_table(stream, renderer, name_heading, columns, rows)


def print_cards(args, cards, stream=None, width=None):
    """
    print one detail card per entry of ``cards``


    :param args: parsed arguments that ran ``add_list_flags``
    :type args: argparse.Namespace
    :param cards: each card is ``(title, remark, fields)``; a field is
            ``(label, text)`` or ``(label, summary, names)``, the names laid
            out in columns below the label line
    :type cards: collections.abc.Iterable[tuple]
    :param stream: output stream; default ``sys.stdout``
    :type stream: IO or None
    :param width: line width to wrap names to; default the terminal's
    :type width: int or None
    """
    stream = stream or sys.stdout
    renderer = _build_renderer(args, stream, FMT_TABLE)
    width = _get_width(width)

    for title, remark, fields in cards:
        head = renderer.color(title, _STYLE_NAME)
        if remark:
            head += renderer.color_grey(": " + remark)
        print(head, file=stream)

        label_width = max((len(field[0]) for field in fields), default=0)
        for field in fields:
            label = renderer.color_grey(field[0].ljust(label_width))
            text = field[1]
            print(_INDENT + label + _COL_GAP + text, file=stream)
            if len(field) == 3:
                for line in _layout_names(field[2], width, len(_INDENT) * 2):
                    print(line, file=stream)


def print_groups(args, groups, stream=None):
    """
    print rows under one bold header per group, names aligned across groups


    :param args: parsed arguments that ran ``add_list_flags``
    :type args: argparse.Namespace
    :param groups: each group is ``(header, rows)``, a row ``(name, remark)``
    :type groups: collections.abc.Iterable[tuple]
    :param stream: output stream; default ``sys.stdout``
    :type stream: IO or None
    """
    stream = stream or sys.stdout
    renderer = _build_renderer(args, stream, FMT_TABLE)
    groups = list(groups)
    name_width = max(
        (len(name) for _, rows in groups for name, _ in rows), default=0
    )

    for header, rows in groups:
        title = "{} ({})".format(header, len(rows))
        print(renderer.color(title, _STYLE_GROUP), file=stream)
        for name, remark in rows:
            line = renderer.color(name.ljust(name_width), _STYLE_NAME)
            if remark:
                line += _NAME_GAP + renderer.color_grey(remark)
            print(_INDENT + line.rstrip(), file=stream)
