"""
list_view.py

define ``add_list_flags``, ``add_name_list_flags``, ``track_given_flags``,
``reject_given_flags``, ``filter_rows``, ``select_columns``,
``print_rows``, ``print_cards``, ``print_groups``, ``print_banner``,
``print_section``, ``print_names``, ``is_human_view``, ``make_renderer``,
``parse_regex`` and ``resolve_format`` -- the shared
mechanism of the informational commands (``affordance``, ``variant``,
``render-profile``, the ``ls`` forms): one flag set, one name filter, table,
tsv, json, card and grouped views, and the comment banner, colored only
through kamilog
"""

import json
import os
import re
import shutil
import sys
from argparse import ArgumentTypeError

import kamilog
from kamilog import AnsiRenderer, AnsiStyle, gen_comment_banner_centered

from kaye_engine import LOGGER_NAME

__all__ = (
    "NAME_LIST_DESTS",
    "FMT_JSON",
    "FMT_TABLE",
    "FMT_TSV",
    "add_format_flag",
    "add_list_flags",
    "add_name_list_flags",
    "filter_rows",
    "is_human_view",
    "make_renderer",
    "parse_regex",
    "print_banner",
    "print_cards",
    "print_groups",
    "print_names",
    "print_rows",
    "print_section",
    "reject_given_flags",
    "resolve_format",
    "select_columns",
    "track_given_flags",
)

logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
# dests of the flags a name list takes, v.i. ``add_name_list_flags``
NAME_LIST_DESTS = ("regex", "names_only", "format", "no_color")
_GIVEN_ATTR = "given_flags"

FMT_TABLE = "table"
FMT_TSV = "tsv"
FMT_JSON = "json"
_FORMATS = (FMT_TABLE, FMT_TSV, FMT_JSON)

_COL_GAP = "  "
_INDENT = "  "
_NAME_GAP = "   "
_DFT_WIDTH = 80
_BANNER_PADDING = 5  # CB5: the lowest, freely usable banner rank

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
            names only; a flag the command lacks counts as unset
    :rtype: bool
    """
    return bool(
        getattr(args, "no_color", False)
        or os.environ.get("NO_COLOR")
        or fmt != FMT_TABLE
        or getattr(args, "names_only", False)
    )


def resolve_format(args, stream):
    """
    :return: ``-f`` when given; otherwise table on a TTY, tsv off one
    :rtype: str
    """
    fmt = getattr(args, "format", None)
    if fmt:
        return fmt
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


def _print_heading(args, stream, heading, count):
    """
    print the list's banner, ``heading: count``, when ``heading`` is given
    and ``stream`` is a TTY; nothing otherwise, so piped output is unchanged
    """
    if heading and is_human_view(stream):
        print_banner(args, "{}: {}".format(heading, count), stream)


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


# auxiliaries  #################################################################
def _add_regex_flag(parser):
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


def _add_names_only_flag(parser):
    parser.add_argument(
        "-N",
        "--names-only",
        action="store_true",
        help="names only, one per line, no heading",
    )


def add_format_flag(parser):
    """
    add ``-f/--format`` to ``parser``


    :param parser: the command's parser
    :type parser: argparse.ArgumentParser
    """
    parser.add_argument(
        "-f",
        "--format",
        choices=_FORMATS,
        help="table (default on a TTY), tsv (default when piped) or json",
    )


def _add_no_color_flag(parser):
    parser.add_argument(
        "-C",
        "--no-color",
        action="store_true",
        help="plain output; NO_COLOR does the same",
    )


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
    _add_regex_flag(parser)
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
    _add_names_only_flag(parser)
    add_format_flag(parser)
    _add_no_color_flag(parser)


def add_name_list_flags(parser):
    """
    add the flags of a plain name list to ``parser``: ``-r/--regex``,
    ``-N/--names-only``, ``-f/--format`` and ``-C/--no-color``, the
    ``add_list_flags`` subset that needs no columns or cards


    :param parser: the name-listing command's parser
    :type parser: argparse.ArgumentParser
    """
    _add_regex_flag(parser)
    _add_names_only_flag(parser)
    add_format_flag(parser)
    _add_no_color_flag(parser)


def track_given_flags(parser, dests):
    """
    make ``parser`` remember which flags of ``dests`` the user typed, so
    ``reject_given_flags`` can tell a flag given from its default

    call it after every argument is added


    :param parser: the command's parser
    :type parser: argparse.ArgumentParser
    :param dests: dests of the flags to remember
    :type dests: collections.abc.Iterable[str]
    """
    dests = frozenset(dests)
    for action in parser._actions:  # pylint: disable=protected-access
        if action.dest not in dests or not action.option_strings:
            continue
        action.__class__ = _build_tracking_class(type(action))


def _build_tracking_class(action_cls):
    class _Tracking(action_cls):
        def __call__(self, parser, namespace, values, option_string=None):
            given = getattr(namespace, _GIVEN_ATTR, None)
            if given is None:
                given = []
                setattr(namespace, _GIVEN_ATTR, given)
            given.append((self.dest, self.option_strings[-1]))
            super().__call__(parser, namespace, values, option_string)

    return _Tracking


def reject_given_flags(args, dests, mode):
    """
    exit 1 naming the first flag of ``dests`` the user typed, when the
    command runs in a mode that ignores it


    :param args: parsed arguments of a parser ``track_given_flags`` ran on
    :type args: argparse.Namespace
    :param dests: dests of the flags the current mode ignores
    :type dests: collections.abc.Iterable[str]
    :param mode: the mode's name, e.g. ``"list mode"``
    :type mode: str
    :raises SystemExit: a flag of ``dests`` was given
    """
    dests = frozenset(dests)
    for dest, flag in getattr(args, _GIVEN_ATTR, None) or ():
        if dest in dests:
            logger.error("%s does not apply in %s", flag, mode)
            raise SystemExit(1)


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


def print_rows(
    args, name_heading, columns, rows, stream=None, heading=None
):
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
    :param heading: banner title, shown with the row count above a table
            on a TTY; default no banner
    :type heading: str or None
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
        _print_heading(args, stream, heading, len(rows))
        _print_table(stream, renderer, name_heading, columns, rows)


def print_cards(args, cards, stream=None, width=None, heading=None):
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
    :param heading: banner title, shown with the card count on a TTY;
            default no banner
    :type heading: str or None
    """
    stream = stream or sys.stdout
    renderer = _build_renderer(args, stream, FMT_TABLE)
    width = _get_width(width)
    cards = list(cards)
    _print_heading(args, stream, heading, len(cards))

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


def print_groups(args, groups, stream=None, heading=None):
    """
    print rows under one bold header per group, names aligned across groups


    :param args: parsed arguments that ran ``add_list_flags``
    :type args: argparse.Namespace
    :param groups: each group is ``(header, rows)``, a row ``(name, remark)``
    :type groups: collections.abc.Iterable[tuple]
    :param stream: output stream; default ``sys.stdout``
    :type stream: IO or None
    :param heading: banner title, shown with the row count on a TTY;
            default no banner
    :type heading: str or None
    """
    stream = stream or sys.stdout
    renderer = _build_renderer(args, stream, FMT_TABLE)
    groups = list(groups)
    _print_heading(
        args, stream, heading, sum(len(rows) for _, rows in groups)
    )
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


def is_human_view(stream=None):
    """
    :param stream: output stream; default ``sys.stdout``
    :type stream: IO or None
    :return: if ``stream`` is a TTY, so a person reads it and banners may
            show; piped output stays machine-friendly
    :rtype: bool
    """
    stream = stream or sys.stdout
    return bool(hasattr(stream, "isatty") and stream.isatty())


def make_renderer(args, stream=None):
    """
    :param args: parsed arguments; ``-C`` and ``NO_COLOR`` switch color off
    :type args: argparse.Namespace
    :param stream: output stream; default ``sys.stdout``
    :type stream: IO or None
    :return: the kamilog renderer for ``stream``; ``None`` when color is
            off: not a TTY, ``-C``, or ``NO_COLOR``
    :rtype: kamilog.AnsiRenderer or None
    """
    stream = stream or sys.stdout
    if not is_human_view(stream) or _is_color_off(args, FMT_TABLE):
        return None
    return _build_renderer(args, stream, FMT_TABLE)


def print_banner(args, heading, stream=None):
    """
    print one centered 80-column comment banner (``CB5C``), its ruler grey
    on a color-enabled TTY


    :param args: parsed arguments; ``-C`` and ``NO_COLOR`` switch color off
    :type args: argparse.Namespace
    :param heading: banner text, a single non-empty line
    :type heading: str
    :param stream: output stream; default ``sys.stdout``
    :type stream: IO or None
    """
    stream = stream or sys.stdout
    renderer = _build_renderer(args, stream, FMT_TABLE)
    print(
        gen_comment_banner_centered(
            heading, _BANNER_PADDING, renderer=renderer
        ),
        file=stream,
    )


def print_section(args, heading, lines, stream=None, is_names=False):
    """
    print a banner over its value lines


    :param args: parsed arguments; ``-C`` and ``NO_COLOR`` switch color off
    :type args: argparse.Namespace
    :param heading: banner text
    :type heading: str
    :param lines: the section's value lines, printed as given
    :type lines: collections.abc.Iterable[str]
    :param stream: output stream; default ``sys.stdout``
    :type stream: IO or None
    :param is_names: whether the lines are names, to print in the name color
    :type is_names: bool
    """
    stream = stream or sys.stdout
    renderer = _build_renderer(args, stream, FMT_TABLE)
    print_banner(args, heading, stream)
    for line in lines:
        print(
            renderer.color(line, _STYLE_NAME) if is_names else line,
            file=stream,
        )


def print_names(args, heading, names, stream=None):
    """
    print ``names`` in the chosen format, after the ``-r`` filter: a table
    is one name per line, in the name color, under a banner; tsv, the
    default when piped, is the bare names, so scripts keep reading one
    name per line; json is an array; ``-N`` always prints bare names


    :param args: parsed arguments; ``-r``, ``-N``, ``-f``, ``-C`` and
            ``NO_COLOR`` apply when the command took
            ``add_name_list_flags``
    :type args: argparse.Namespace
    :param heading: banner text, shown with the count above a table
    :type heading: str
    :param names: the names, printed in the order given
    :type names: collections.abc.Iterable[str]
    :param stream: output stream; default ``sys.stdout``
    :type stream: IO or None
    """
    stream = stream or sys.stdout
    names = [
        name
        for name in names
        if not getattr(args, "regex", None)
        or any(pat.search(name) for pat in args.regex)
    ]
    fmt = resolve_format(args, stream)

    if fmt == FMT_JSON and not getattr(args, "names_only", False):
        print(json.dumps(names, indent=2, ensure_ascii=False), file=stream)
    elif fmt == FMT_TABLE and not getattr(args, "names_only", False):
        print_section(
            args,
            "{}: {}".format(heading, len(names)),
            names,
            stream,
            is_names=True,
        )
    else:
        for name in names:
            print(name, file=stream)
