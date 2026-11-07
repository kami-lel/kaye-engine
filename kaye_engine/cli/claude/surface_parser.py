"""
surface_parser.py

define ``build_surface_parent_parser`` -- a shared argparse parent parser
adding the ``--surface`` flag, reused as a `parents=[...]` entry by each
``kaye claude`` subcommand instead of repeating ``add_argument`` per
subcommand
"""

from argparse import ArgumentParser

from kaye_engine.prompt.blueprint.render_profile_registry import (
    render_profile_registry,
)

__all__ = ("build_surface_parent_parser",)


# Main Entry Point  ############################################################
def build_surface_parent_parser(default):
    """
    build a fresh, help-suppressed ``ArgumentParser`` carrying only the
    ``--surface`` flag, its choices the names in
    ``render_profile_registry`` (the flag is omitted when none is
    registered), for use as a `parents=[...]` entry -- a fresh
    instance per call avoids `parents=` option-string conflicts across
    the several subcommands sharing this builder


    :param default: member names checkmarked when ``--surface`` is
            omitted
    :type default: Iterable[str]
    :return: the parent parser
    :rtype: ArgumentParser
    """
    parent = ArgumentParser(add_help=False)
    if render_profile_registry:
        parent.add_argument(
            "-u",
            "--surface",
            nargs="+",
            metavar="SURFACE",
            choices=list(render_profile_registry),
            default=list(default),
            help="Claude surface(s) to checkmark for; combinable, v.s.",
        )
    return parent
