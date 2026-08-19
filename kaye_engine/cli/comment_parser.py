"""
comment_parser.py

define ``build_comment_parent_parser`` -- a shared argparse parent parser
adding the ``--comment``/``--no-comment`` mutually-exclusive pair, reused
as a `parents=[...]` entry by ``blueprint show`` directly and, composed
via ``render_profile_parser.py``, by every rendering command
"""

from argparse import ArgumentParser

__all__ = ("build_comment_parent_parser",)


# Main Entry Point  ############################################################
def build_comment_parent_parser(*, short_flags=True):
    """
    build a fresh, help-suppressed ``ArgumentParser`` carrying the
    ``--comment``/``--no-comment`` mutually-exclusive pair -- a fresh
    instance per call avoids `parents=` option-string conflicts across
    the several subcommands sharing this builder

    both flags default ``dest="show_comment"`` to ``None`` so the caller
    can fall back to its own pre-existing default when neither flag is
    passed


    :param short_flags: whether to also register ``-c``/``-C`` --
            ``False`` for ``claude user-system-prompt``, which already
            owns ``-c`` for ``--coder``
    :type short_flags: bool
    :return: the parent parser
    :rtype: ArgumentParser
    """
    parent = ArgumentParser(add_help=False)
    group = parent.add_mutually_exclusive_group()
    comment_flags = ["-c", "--comment"] if short_flags else ["--comment"]
    no_comment_flags = (
        ["-C", "--no-comment"] if short_flags else ["--no-comment"]
    )
    group.add_argument(
        *comment_flags,
        dest="show_comment",
        action="store_true",
        default=None,
        help="show comment nodes in the rendered output",
    )
    group.add_argument(
        *no_comment_flags,
        dest="show_comment",
        action="store_false",
        default=None,
        help="omit comment nodes from the rendered output",
    )
    return parent
