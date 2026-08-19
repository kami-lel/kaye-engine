"""
surface_parser.py

define ``build_surface_parent_parser`` -- a shared argparse parent parser
adding the ``--surface`` flag, reused as a `parents=[...]` entry by each
``kaye claude`` subcommand instead of repeating ``add_argument`` per
subcommand
"""

from argparse import ArgumentParser

__all__ = ("build_surface_parent_parser",)


# Main Entry Point  ############################################################
def build_surface_parent_parser(default, *, surface_profiles=None):
    """
    build a fresh, help-suppressed ``ArgumentParser`` carrying only the
    ``--surface`` flag, for use as a `parents=[...]` entry -- a fresh
    instance per call avoids `parents=` option-string conflicts across
    the several subcommands sharing this builder


    :param default: member names checkmarked when ``--surface`` is
            omitted
    :type default: Iterable[str]
    :param surface_profiles: populates the ``--surface`` flag's
            choices; ``None`` or empty omits ``--surface`` entirely --
            precedented by ``default_surface=()`` for surface-less
            subcommands
    :type surface_profiles: dict[str, RenderProfile] or None, optional
    :return: the parent parser
    :rtype: ArgumentParser
    """
    parent = ArgumentParser(add_help=False)
    if surface_profiles:
        parent.add_argument(
            "-u",
            "--surface",
            nargs="+",
            metavar="SURFACE",
            choices=list(surface_profiles),
            default=list(default),
            help="Claude surface(s) to checkmark for; combinable",
        )
    return parent
