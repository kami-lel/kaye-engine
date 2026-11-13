"""
comment_parser.py

define ``build_comment_parent_parser`` -- a shared argparse parent parser
adding the ``--comment``/``--no-comment`` mutually-exclusive pair, long
form only (``-C`` belongs to ``--no-color``), reused
as a `parents=[...]` entry by ``blueprint show`` directly and, composed
via ``render_profile_parser.py``, by every rendering command
"""

from argparse import ArgumentParser

__all__ = ("build_comment_parent_parser",)


# Main Entry Point  ############################################################
def build_comment_parent_parser(*, is_render_profile=False):
    """
    build a fresh, help-suppressed ``ArgumentParser`` carrying the
    ``--comment``/``--no-comment`` mutually-exclusive pair -- a fresh
    instance per call avoids `parents=` option-string conflicts across
    the several subcommands sharing this builder

    both flags default ``dest="show_comment"`` to ``None`` so the caller
    can fall back to its own pre-existing default when neither flag is
    passed


    :param is_render_profile: whether the flags belong to the render
            profile options, appending ``v.s.`` to their help
    :type is_render_profile: bool
    :return: the parent parser
    :rtype: ArgumentParser
    """
    parent = ArgumentParser(add_help=False)
    vs = ", v.s." if is_render_profile else ""
    group = parent.add_mutually_exclusive_group()
    group.add_argument(
        "--comment",
        dest="show_comment",
        action="store_true",
        default=None,
        help="show comment nodes in the rendered output" + vs,
    )
    group.add_argument(
        "--no-comment",
        dest="show_comment",
        action="store_false",
        default=None,
        help="omit comment nodes from the rendered output" + vs,
    )
    return parent
