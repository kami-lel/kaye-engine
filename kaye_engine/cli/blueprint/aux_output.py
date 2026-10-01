"""
aux_output.py

define ``SHOW_FIELD_FXS``, ``pick_preview_fx``, ``pick_render_fx``,
``pick_show_fx``, ``fmt_ls``, ``fmt_summary``, ``fmt_show_result``,
``emit_str``, ``run_cmd``, ``run_cmd_and_exit`` -- the CLI glue between
API functions and stdout; each one composes API functions, none
duplicates their logic
"""

import kamilog
from kaye_engine import LOGGER_NAME
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


def _show_summary(blueprint):
    """
    :type blueprint: Blueprint
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


def pick_show_fx(field):
    """
    :param field: field flag name of ``bp show``, ``None`` for none
    :type field: str or None
    :raises KeyError: an unknown field name
    :return: the show function for the flag; the summary text for none
    :rtype: Callable
    """
    if field is None:
        return _show_summary

    return SHOW_FIELD_FXS[field]


def fmt_ls(names):
    """
    :type names: Iterable[str]
    :return: the names, one per line
    :rtype: str
    """
    return "\n".join(names)


def fmt_summary(
    summary, *, description="", when_to_use="", nodes=(), subtrees=()
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
    :return: the summary as fields, each a centered banner line over its
            value lines; a text field with no value is left out, while
            ``nodes`` and ``subtrees`` always show their count
    :rtype: str
    """
    text_fields = (
        ("display name", summary.meta.display_name),
        ("description", description),
        (
            "description node",
            _gen_lineage_str(summary.meta.description_node),
        ),
        ("when to use", when_to_use),
        (
            "when to use node",
            _gen_lineage_str(summary.meta.when_to_use_node),
        ),
    )

    lines = []
    for label, value in text_fields:
        if value:
            lines += [kamilog.gen_comment_banner_centered(label, 5), value]

    for label, count, paths in (
        ("nodes", summary.node_count, nodes),
        ("subtrees", summary.subtree_count, subtrees),
    ):
        heading = "{}: {}".format(label, count)
        lines.append(kamilog.gen_comment_banner_centered(heading, 5))
        lines += _gen_lineage_strs(paths)

    if summary.dependencies:
        lines.append(kamilog.gen_comment_banner_centered("dependencies", 5))
        lines.append(fmt_ls(summary.dependencies))

    return fmt_ls(lines)


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
        logger.critical(str(err.args[0] if err.args else err))
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
