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
# ``bp show`` field flag name -> the API function it selects
SHOW_FIELD_FXS = {
    "description": show_description,
    "when-to-use": show_when_to_use,
    "globs": show_globs,
    "dependencies": show_dependencies,
}

_NONE_LABEL = "-"
_PATH_SEPARATOR = " > "


# auxiliaries  #################################################################
def _fmt_path(path):
    return _PATH_SEPARATOR.join(path) if path else _NONE_LABEL


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
    :return: the show function for the flag; ``show_blueprint`` for none
    :rtype: Callable
    """
    if field is None:
        return show_blueprint

    return SHOW_FIELD_FXS[field]


def fmt_ls(names):
    """
    :type names: Iterable[str]
    :return: the names, one per line
    :rtype: str
    """
    return "\n".join(names)


def fmt_summary(summary):
    """
    :type summary: BlueprintSummary
    :return: the summary as ``label: value`` lines; ``-`` for what is
            not set
    :rtype: str
    """
    meta = summary.meta

    return fmt_ls(
        [
            "description: {}".format(meta.description or _NONE_LABEL),
            "description-node: {}".format(_fmt_path(meta.description_node)),
            "when-to-use-node: {}".format(_fmt_path(meta.when_to_use_node)),
            "globs-node: {}".format(_fmt_path(meta.globs_node)),
            "nodes: {}".format(summary.node_count),
            "subtrees: {}".format(summary.subtree_count),
            "dependencies: {}".format(
                ", ".join(summary.dependencies) or _NONE_LABEL
            ),
        ]
    )


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
