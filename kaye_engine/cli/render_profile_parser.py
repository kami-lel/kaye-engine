"""
render_profile_parser.py

define ``build_render_profile_parent_parser`` and
``resolve_render_profile`` -- the shared parent parser and aux function
behind the 5 render options (``--surface``, ``--comment``/
``--no-comment``, ``--conditional-sidecar``, ``--affordance``,
``--sparseness``) every rendering command exposes
"""

from argparse import ArgumentParser

from kaye_engine.cli.comment_parser import build_comment_parent_parser
from kaye_engine.cli.sparseness_parser import build_sparseness_parent_parser
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude.surface_parser import build_surface_parent_parser
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


def resolve_render_profile(
    args, *, surface_profiles=None, default_show_comment=False
):
    """
    resolve a parsed ``Namespace`` carrying the 5 render options into a
    `RenderProfile`, directly ``**``-splattable via ``as_kwargs()`` or
    passable as ``profile=`` into ``generate_prompt(...)``/
    ``BlueprintRegistry.content(...)``


    :param args: namespace parsed from a parser built by
            ``build_render_profile_parent_parser``
    :type args: argparse.Namespace
    :param surface_profiles: same dict passed to
            ``build_render_profile_parent_parser``, used to resolve
            ``args.surface`` names into their `RenderProfile`; unused
            (and ``args`` has no ``surface`` attribute) when
            ``--surface`` was omitted
    :type surface_profiles: dict[str, RenderProfile] or None, optional
    :param default_show_comment: fallback used when neither
            ``--comment`` nor ``--no-comment`` was passed -- each
            call site states its own pre-existing default
    :type default_show_comment: bool
    :return: resolved render profile; a caller-side registry's own
            `render_profile` is still merged in on top rather than
            being replaced (see ``BlueprintRegistry.content()``)
    :rtype: RenderProfile
    """
    show_comment = (
        default_show_comment
        if args.show_comment is None
        else args.show_comment
    )

    surface_names = getattr(args, "surface", None) or ()

    profile = RenderProfile()
    for name in surface_names:
        profile = profile.merge(surface_profiles[name])

    if args.affordance or surface_names:
        profile = profile.merge(
            RenderProfile(affordances=tuple(args.affordance))
        )
    if args.conditional_sidecar:
        profile = profile.merge(
            RenderProfile(
                conditional_sidecars=tuple(args.conditional_sidecar)
            )
        )

    return profile.merge(
        RenderProfile(sparseness=args.sparseness, show_comment=show_comment)
    )
