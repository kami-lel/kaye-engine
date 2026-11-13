"""
aux_output.py

define ``SHOW_FIELD_FXS``, ``pick_preview_fx``, ``pick_render_fx``,
``pick_show_fx``, ``fmt_ls``, ``fmt_summary``, ``fmt_show_result``,
``emit_str``, ``run_cmd``, ``run_cmd_and_exit`` -- the CLI glue between
API functions and stdout; each one composes API functions, none
duplicates their logic
"""

import json
from functools import partial

import kamilog
from kaye_engine import LOGGER_NAME
from kaye_engine.cli.list_view import FMT_JSON, FMT_TABLE, FMT_TSV
from kaye_engine.prompt.blueprint import (
    BlueprintSummary,
    preview_blueprint,
    preview_blueprint_without_dependencies,
    render_prompt,
    render_prompt_without_dependencies,
    show_blueprint,
    show_dependencies,
    show_description,
    show_display_name,
    show_globs,
    show_when_to_use,
)

__all__ = (
    "SHOW_FIELD_FXS",
    "emit_str",
    "fmt_ls",
    "fmt_strip_trailing_space",
    "fmt_show_result",
    "fmt_summary",
    "pick_preview_fx",
    "pick_render_fx",
    "pick_show_fx",
    "run_cmd",
    "run_cmd_and_exit",
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


# constants  ###################################################################
_LINEAGE_SEPARATOR = " # "
_INDENT = "  "
_BANNER_PADDING = 5  # CB5


# auxiliaries  #################################################################
def _gen_lineage_str(path):
    """
    :param path: node path, ``None`` for no node
    :type path: NodePath or None
    :return: the path's names joined by `` # ``, ``""`` for no node
    :rtype: str
    """
    return _LINEAGE_SEPARATOR.join(path or ())


def _gen_lineage_strs(paths):
    """
    :type paths: Iterable[NodePath]
    :return: each path's lineage string, sorted
    :rtype: list[str]
    """
    return sorted(_gen_lineage_str(path) for path in paths)


def _show_from_summary(fmt_fx):
    """
    :param fmt_fx: formats a ``BlueprintSummary`` into the one field
    :type fmt_fx: Callable
    :return: a show function for that field, reading the summary
    :rtype: Callable
    """
    return lambda blueprint: fmt_fx(show_blueprint(blueprint))


def _show_summary(blueprint, renderer=None, fmt=FMT_TABLE):
    """
    :type blueprint: Blueprint
    :param renderer: colors a table summary; ``None`` for plain text
    :type renderer: kamilog.AnsiRenderer or None
    :param fmt: table, tsv or json
    :type fmt: str
    :raises ValueError: a meta node is not in the loaded corpus
    :return: the summary text, with description and when-to-use as content
    :rtype: str
    """
    return fmt_summary(
        show_blueprint(blueprint),
        description=show_description(blueprint),
        when_to_use=show_when_to_use(blueprint),
        nodes=blueprint.nodes,
        subtrees=blueprint.subtrees,
        renderer=renderer,
        fmt=fmt,
    )


# constants  ###################################################################
# ``bp show`` field flag name -> the API function it selects
SHOW_FIELD_FXS = {
    "display-name": show_display_name,
    "description": show_description,
    "description-node": _show_from_summary(
        lambda summary: _gen_lineage_str(summary.meta.description_node)
    ),
    "when-to-use": show_when_to_use,
    "when-to-use-node": _show_from_summary(
        lambda summary: _gen_lineage_str(summary.meta.when_to_use_node)
    ),
    "nodes": lambda blueprint: _gen_lineage_strs(blueprint.nodes),
    "subtrees": lambda blueprint: _gen_lineage_strs(blueprint.subtrees),
    "globs": show_globs,
    "dependencies": show_dependencies,
}


# Public API  ##################################################################
def pick_preview_fx(is_no_dependencies):
    """
    :param is_no_dependencies: whether ``-D`` is set
    :type is_no_dependencies: bool
    :return: the preview function for the flag
    :rtype: Callable
    """
    if is_no_dependencies:
        return preview_blueprint_without_dependencies

    return preview_blueprint


def pick_render_fx(is_no_dependencies):
    """
    :param is_no_dependencies: whether ``-D`` is set
    :type is_no_dependencies: bool
    :return: the render function for the flag
    :rtype: Callable
    """
    if is_no_dependencies:
        return render_prompt_without_dependencies

    return render_prompt


def pick_show_fx(field, renderer=None, fmt=FMT_TABLE):
    """
    :param field: field name of ``bp show -F``, ``None`` for none
    :type field: str or None
    :param renderer: colors the summary only; a field always prints raw
    :type renderer: kamilog.AnsiRenderer or None
    :param fmt: the summary's format; a field always prints raw
    :type fmt: str
    :raises KeyError: an unknown field name
    :return: the show function for the flag; the summary text for none
    :rtype: Callable
    """
    if field is None:
        return partial(_show_summary, renderer=renderer, fmt=fmt)

    return SHOW_FIELD_FXS[field]


def fmt_ls(names):
    """
    :type names: Iterable[str]
    :return: the names, one per line
    :rtype: str
    """
    return "\n".join(names)


def _style_lineage(renderer, lineage):
    """
    :return: ``lineage`` with the name color on its names and grey
            separators
    :rtype: str
    """
    names = lineage.split(_LINEAGE_SEPARATOR)
    return renderer.color_grey(_LINEAGE_SEPARATOR).join(
        renderer.color(name, kamilog.AnsiStyle.BRIGHT_CYAN) for name in names
    )


def _gen_summary_fields(summary, description, when_to_use, nodes, subtrees):
    """
    :return: the summary's fields in print order, each ``(key, kind,
            value)``: ``key`` the ``--field`` name, also the banner and tsv
            label, ``kind`` ``text``,
            ``lineage`` (a text that is one lineage) or ``names`` (a list)
    :rtype: list[tuple]
    """
    return [
        ("display-name", "text", summary.meta.display_name),
        ("description", "text", description),
        (
            "description-node",
            "lineage",
            _gen_lineage_str(summary.meta.description_node),
        ),
        ("when-to-use", "text", when_to_use),
        (
            "when-to-use-node",
            "lineage",
            _gen_lineage_str(summary.meta.when_to_use_node),
        ),
        ("nodes", "names", _gen_lineage_strs(nodes)),
        ("subtrees", "names", _gen_lineage_strs(subtrees)),
        ("dependencies", "names", list(summary.dependencies)),
    ]


def _fmt_summary_table(fields, summary, renderer):
    """
    :return: the table view: each field a centered banner over its
            indented value lines; a text field with no value and an empty
            dependency list are left out, while ``nodes`` and ``subtrees``
            always show their count
    :rtype: str
    """

    def banner(heading):
        return kamilog.gen_comment_banner_centered(
            heading, _BANNER_PADDING, renderer=renderer
        )

    def style(value):
        return value if renderer is None else _style_lineage(renderer, value)

    counts = {"nodes": summary.node_count, "subtrees": summary.subtree_count}
    lines = []
    for key, kind, value in fields:
        if kind == "names":
            label = key
            if key in counts:
                label = "{} ({})".format(key, counts[key])
            elif not value:
                continue
            lines.append(banner(label))
            lines += [_INDENT + style(name) for name in value]
        elif value:
            lines.append(banner(key))
            if kind == "lineage":
                lines.append(_INDENT + style(value))
            else:
                lines += [_INDENT + line for line in value.splitlines()]

    return fmt_ls(lines)


def _fmt_summary_tsv(fields):
    """
    :return: ``key<TAB>value`` rows, one per list item; a multi-line text
            keeps to one row with its newlines written ``\\n``
    :rtype: str
    """
    rows = []
    for key, kind, value in fields:
        values = value if kind == "names" else [value] if value else []
        rows += [
            "{}\t{}".format(key, text.replace("\n", "\\n"))
            for text in values
        ]
    return fmt_ls(rows)


def fmt_summary(
    summary,
    *,
    description="",
    when_to_use="",
    nodes=(),
    subtrees=(),
    renderer=None,
    fmt=FMT_TABLE
):
    """
    :type summary: BlueprintSummary
    :param description: description content, ``""`` for none
    :type description: str
    :param when_to_use: when-to-use content, ``""`` for none
    :type when_to_use: str
    :param nodes: paths of the nodes checkmarked one by one
    :type nodes: Iterable[NodePath]
    :param subtrees: paths of the nodes checkmarked with their descendants
    :type subtrees: Iterable[NodePath]
    :param renderer: colors the table view: grey banner rulers and names in
            the name color; ``None`` for plain text
    :type renderer: kamilog.AnsiRenderer or None
    :param fmt: ``table`` (banner-headed fields over indented values),
            ``tsv`` (``key<TAB>value`` rows) or ``json`` (one object of
            every field)
    :type fmt: str
    :return: the summary in that format
    :rtype: str
    """
    fields = _gen_summary_fields(
        summary, description, when_to_use, nodes, subtrees
    )

    if fmt == FMT_JSON:
        record = {key: value for key, _kind, value in fields}
        return json.dumps(record, indent=2, ensure_ascii=False)

    if fmt == FMT_TSV:
        return _fmt_summary_tsv(fields)

    return _fmt_summary_table(fields, summary, renderer)


def fmt_show_result(result):
    """
    :param result: what a show function returned
    :type result: str or tuple[str, ...] or list[str] or BlueprintSummary
    :return: the text ``bp show`` prints for it
    :rtype: str
    """
    if isinstance(result, BlueprintSummary):
        return fmt_summary(result)

    if isinstance(result, str):
        return result

    return fmt_ls(result)


def fmt_strip_trailing_space(text):
    """
    :param text: multi-line text
    :type text: str
    :return: ``text`` with the trailing blanks of every line cut, so no
            printed line ends in whitespace
    :rtype: str
    """
    return "\n".join(line.rstrip() for line in text.split("\n"))


def emit_str(text):
    """
    :param text: text to print to stdout
    :type text: str
    """
    print(text)


def run_cmd(handler, args):
    """
    :param handler: the command handler
    :type handler: Callable
    :param args: parsed arguments, passed to ``handler``
    :type args: argparse.Namespace
    :return: ``0``, or ``1`` after logging the error a handler raised as
            ``ValueError``, ``KeyError``, or ``FileNotFoundError``
    :rtype: int
    """
    try:
        handler(args)
    except (ValueError, KeyError, FileNotFoundError) as err:
        logger.error(str(err.args[0] if err.args else err))
        return 1

    return 0


def run_cmd_and_exit(handler, args):
    """
    run ``handler`` through :func:`run_cmd`, and leave the process with its
    exit code when that is not ``0``


    :param handler: the command handler
    :type handler: Callable
    :param args: parsed arguments, passed to ``handler``
    :type args: argparse.Namespace
    :raises SystemExit: the handler failed
    """
    exit_code = run_cmd(handler, args)

    if exit_code:
        raise SystemExit(exit_code)
