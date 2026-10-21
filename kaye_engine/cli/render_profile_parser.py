"""
render_profile_parser.py

define ``build_render_profile_parent_parser`` and
``resolve_render_profile`` -- the shared parent parser and aux function
behind the 6 render options (``--surface``, ``--comment``/
``--no-comment``, ``--conditional-sidecar``, ``--variant``,
``--sparseness``, ``--reverse-order``) every rendering command exposes
"""

from argparse import ArgumentParser

from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude.surface_parser import build_surface_parent_parser
from kaye_engine.cli.comment_parser import build_comment_parent_parser
from kaye_engine.cli.sparseness_parser import build_sparseness_parent_parser
from kaye_engine.prompt.blueprint.render_mode import RenderMode
from kaye_engine.prompt.blueprint.render_profile import RenderProfile

__all__ = (
    "build_render_profile_parent_parser",
    "resolve_render_profile",
)


# Main Entry Point  ############################################################
def build_render_profile_parent_parser(
    *,
    default_surface=(),
    default_sparseness=DEFAULT_SPARSENESS,
    comment_short_flags=True,
    surface_profiles=None,
):
    """
    build a fresh, help-suppressed ``ArgumentParser`` carrying all 6
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
    :param surface_profiles: populates the ``--surface`` flag's
            choices; ``None`` or empty omits ``--surface`` entirely
    :type surface_profiles: dict[str, RenderProfile] or None, optional
    :return: the parent parser
    :rtype: ArgumentParser
    """
    parent = ArgumentParser(
        add_help=False,
        parents=[
            build_surface_parent_parser(
                default_surface, surface_profiles=surface_profiles
            ),
            build_sparseness_parent_parser(default_sparseness),
            build_comment_parent_parser(
                short_flags=comment_short_flags, is_render_profile=True
            ),
        ],
    )
    parent.add_argument(
        "--variant",
        nargs="+",
        metavar="VARIANT",
        default=(),
        help="variant name(s) to include, v.s.",
    )
    parent.add_argument(
        "-i",
        "--conditional-sidecar",
        nargs="+",
        metavar="SIDECAR",
        default=(),
        help="conditional-sidecar name(s) to include, v.s.",
    )
    parent.add_argument(
        "--reverse-order",
        dest="reverse_sibling_order",
        action="store_true",
        default=False,
        help="reverse sibling order, v.s.",
    )
    return parent


def resolve_render_profile(
    args, *, surface_profiles=None, default_show_comment=False
):
    """
    resolve the parsed render options into a ``RenderProfile``


    :param args: namespace from a parser built by
            ``build_render_profile_parent_parser``
    :type args: argparse.Namespace
    :param surface_profiles: profiles keyed by ``--surface`` name;
            same dict given to the parser builder
    :type surface_profiles: dict{str: RenderProfile}, optional
    :param default_show_comment: whether to show the comment when
            neither ``--comment`` nor ``--no-comment`` was passed;
            default=False
    :type default_show_comment: bool, optional
    :return: resolved render profile
    :rtype: RenderProfile
    """
    show_comment = (
        default_show_comment if args.show_comment is None else args.show_comment
    )

    surface_names = getattr(args, "surface", None) or ()

    profile = RenderProfile()
    for name in surface_names:
        profile = profile.merge(surface_profiles[name])

    if args.variant or surface_names:
        profile = profile.merge(RenderProfile(variants=tuple(args.variant)))
    if args.conditional_sidecar:
        profile = profile.merge(
            RenderProfile(conditional_sidecars=tuple(args.conditional_sidecar))
        )

    mode = profile.mode
    if args.reverse_sibling_order:
        mode |= RenderMode.REVERSE_ORDER

    return profile.merge(
        RenderProfile(
            sparseness=args.sparseness, show_comment=show_comment, mode=mode
        )
    )
