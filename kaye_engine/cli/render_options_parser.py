"""
render_options_parser.py

define ``build_render_options_parent_parser`` and
``resolve_render_options`` -- the shared parent parser and aux function
behind the 5 render options (``--surface``, ``--comment``/
``--no-comment``, ``--conditional-sidecar``, ``--affordance``,
``--sparseness``) every rendering command exposes
"""

from argparse import ArgumentParser

from kaye_engine.cli.comment_parser import build_comment_parent_parser
from kaye_engine.cli.sparseness_parser import build_sparseness_parent_parser
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude.surface_parser import build_surface_parent_parser
from kaye_engine.prompt.claude_surface import ClaudeSurface

__all__ = (
    "build_render_options_parent_parser",
    "resolve_render_options",
)


# Main Entry Point  ############################################################
def build_render_options_parent_parser(
    *,
    default_surface=(),
    default_sparseness=DEFAULT_SPARSENESS,
    comment_short_flags=True,
):
    """
    build a fresh, help-suppressed ``ArgumentParser`` carrying all 5
    render options -- for use as a `parents=[...]` entry -- a fresh
    instance per call avoids `parents=` option-string conflicts across
    the several subcommands sharing this builder


    :param default_surface: member names checkmarked when ``--surface``
            is omitted; empty for surface-less subcommands
    :type default_surface: Iterable[str]
    :param default_sparseness: sparseness value used when
            ``--sparseness`` is omitted
    :type default_sparseness: int or None
    :param comment_short_flags: whether ``--comment``/``--no-comment``
            also register ``-c``/``-C``, v.s. ``build_comment_parent_
            parser``
    :type comment_short_flags: bool
    :return: the parent parser
    :rtype: ArgumentParser
    """
    parent = ArgumentParser(
        add_help=False,
        parents=[
            build_surface_parent_parser(default_surface),
            build_sparseness_parent_parser(default_sparseness),
            build_comment_parent_parser(short_flags=comment_short_flags),
        ],
    )
    parent.add_argument(
        "-a",
        "--affordance",
        nargs="+",
        metavar="AFFORDANCE",
        default=(),
        help="affordance name(s) to include, unioned with --surface",
    )
    parent.add_argument(
        "-i",
        "--conditional-sidecar",
        nargs="+",
        metavar="SIDECAR",
        default=(),
        help=(
            "conditional-sidecar name(s) to include, unioned with "
            "--surface"
        ),
    )
    return parent


def resolve_render_options(args, *, default_show_comment=False):
    """
    resolve a parsed ``Namespace`` carrying the 5 render options into a
    kwargs dict directly ``**``-splattable into
    ``generate_prompt(...)``


    :param args: namespace parsed from a parser built by
            ``build_render_options_parent_parser``
    :type args: argparse.Namespace
    :param default_show_comment: fallback used when neither
            ``--comment`` nor ``--no-comment`` was passed -- each
            call site states its own pre-existing default
    :type default_show_comment: bool
    :return: kwargs for ``generate_prompt(...)``; ``affordances``/
            ``conditional_sidecars`` are omitted entirely (rather than set
            to their empty defaults) when neither the corresponding flag
            nor ``--surface`` was passed; when present, a registry-level
            default (see ``BlueprintRegistry.content()``) is still merged
            in on top rather than being replaced
    :rtype: dict
    """
    surface = ClaudeSurface.combine(args.surface) if args.surface else None

    show_comment = (
        default_show_comment
        if args.show_comment is None
        else args.show_comment
    )

    result = {
        "sparseness": args.sparseness,
        "show_comment": show_comment,
    }

    if surface is None:
        if args.affordance:
            result["affordances"] = tuple(args.affordance)
        if args.conditional_sidecar:
            result["conditional_sidecars"] = tuple(args.conditional_sidecar)
    else:
        result["affordances"] = tuple(
            dict.fromkeys(
                (*surface.as_affordances(), *args.affordance)
            )
        )
        result["conditional_sidecars"] = tuple(
            dict.fromkeys(
                (*surface.as_contained_sidecars(), *args.conditional_sidecar)
            )
        )

    return result
