"""
list_table.py

define ``add_info_flags``, ``select_info_columns`` and ``print_table`` --
the shared mechanism of the list commands (``affordance``, ``variant``,
``render-profile``) that print a name column plus optional info columns
under a heading line
"""

__all__ = (
    "add_info_flags",
    "print_table",
    "select_info_columns",
)

# constants  ###################################################################
_EVENT_ALL = "all"
_EVENT_NONE = "none"
_EVENTS_DEST = "info_events"


# Public API  ##################################################################
def add_info_flags(parser, info_columns):
    """
    add ``-i/--info``, ``-I/--no-info`` and one flag per info column to
    ``parser``; every flag records itself in order, so the last one wins


    :param parser: the list command's parser
    :type parser: argparse.ArgumentParser
    :param info_columns: column key -> ``(short_flag, long_flag)`` or
            ``None`` when the column has no flag of its own; the key is
            also the column's heading
    :type info_columns: dict
    """
    parser.add_argument(
        "-i",
        "--info",
        dest=_EVENTS_DEST,
        action="append_const",
        const=_EVENT_ALL,
        help="show every info column (default)",
    )
    parser.add_argument(
        "-I",
        "--no-info",
        dest=_EVENTS_DEST,
        action="append_const",
        const=_EVENT_NONE,
        help="show names only, with no heading line",
    )

    for key, flags in info_columns.items():
        if flags is None:
            continue
        short_flag, long_flag = flags
        parser.add_argument(
            short_flag,
            long_flag,
            dest=_EVENTS_DEST,
            action="append_const",
            const=key,
            help="show the {} column".format(key),
        )


def select_info_columns(args, info_columns):
    """
    resolve the flags the user gave into the info columns to print


    :param args: parsed arguments of a list command that ran
            ``add_info_flags``
    :type args: argparse.Namespace
    :param info_columns: the same ``info_columns`` given to
            ``add_info_flags``
    :type info_columns: dict
    :return: the selected column keys, in ``info_columns`` order; every
            column when no flag was given
    :rtype: list[str]
    """
    events = getattr(args, _EVENTS_DEST, None)
    if not events:
        return list(info_columns)

    selected = set()
    for event in events:
        if event == _EVENT_ALL:
            selected = set(info_columns)
        elif event == _EVENT_NONE:
            selected.clear()
        else:
            selected.add(event)

    return [key for key in info_columns if key in selected]


def print_table(name_heading, selected, rows):
    """
    print ``rows`` as tab-separated columns: a heading line first, unless
    no info column is selected, then one line per row


    :param name_heading: heading of the name column
    :type name_heading: str
    :param selected: info column keys to print, in order
    :type selected: list[str]
    :param rows: each row is ``(name, {column key: cell text})``, in print
            order
    :type rows: collections.abc.Iterable[tuple]
    """
    if selected:
        print("\t".join([name_heading, *selected]))

    for name, cells in rows:
        print("\t".join([name, *(cells[key] for key in selected)]))
