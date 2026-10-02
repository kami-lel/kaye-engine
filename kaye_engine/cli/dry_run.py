"""
dry_run.py

define ``build_dry_run_parent_parser``, ``enable_dry_run``, and
``is_dry_run`` -- the shared ``--dry-run`` flag of every command that
writes to disk, and the run-wide switch its writers consult before
touching the filesystem
"""

import kamilog
from argparse import ArgumentParser

from kaye_engine import LOGGER_NAME
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.continue_ai import LOGGER_CONTINUE_NAME
from kaye_engine.cli.hermes import LOGGER_HERMES_NAME
from kaye_engine.cli.open_webui import LOGGER_OPEN_WEBUI_NAME
from kaye_engine.skill import LOGGER_SKILL_NAME

__all__ = (
    "DRY_BADGE",
    "build_dry_run_parent_parser",
    "enable_dry_run",
    "apply_dry_run_arg",
    "disable_dry_run",
    "is_dry_run",
)


# constants  ###################################################################
DRY_BADGE = "dry"

_LOGGER_NAMES = (
    LOGGER_NAME,
    LOGGER_CLAUDE_NAME,
    LOGGER_CONTINUE_NAME,
    LOGGER_HERMES_NAME,
    LOGGER_OPEN_WEBUI_NAME,
    LOGGER_SKILL_NAME,
)

# run-wide switch; writers read it through is_dry_run()
_is_dry_run_enabled = False


# Main Entry Point  ############################################################
def build_dry_run_parent_parser():
    """
    build a fresh, help-suppressed ``ArgumentParser`` carrying only the
    ``-n/--dry-run`` flag, for use as a `parents=[...]` entry

    :return: the parent parser
    :rtype: ArgumentParser
    """
    parent = ArgumentParser(add_help=False)
    parent.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="plan and report every write with the dry badge, change"
        " nothing on disk",
    )
    return parent


def enable_dry_run():
    """
    switch the run to dry: every engine logger carries the ``dry``
    badge and :func:`is_dry_run` turns true
    """
    global _is_dry_run_enabled
    _is_dry_run_enabled = True
    for name in _LOGGER_NAMES:
        kamilog.getLogger(name).set_badges(DRY_BADGE)


def disable_dry_run():
    """
    switch the run back to live: drop the ``dry`` badge from every
    engine logger and turn :func:`is_dry_run` false
    """
    global _is_dry_run_enabled
    _is_dry_run_enabled = False
    for name in _LOGGER_NAMES:
        kamilog.getLogger(name).clear_badges()


def apply_dry_run_arg(args):
    """
    set the run-wide switch from a parsed namespace, so a command's main
    starts every run in a known mode

    :param args: parsed namespace carrying ``dry_run``
    :type args: argparse.Namespace
    """
    if getattr(args, "dry_run", False):
        enable_dry_run()
    else:
        disable_dry_run()


def is_dry_run():
    """
    :return: if writers must report only and leave the filesystem alone
    :rtype: bool
    """
    return _is_dry_run_enabled
