"""
blueprint_arg_parser.py

define ``build_blueprint_arg_parser``, ``build_no_dependencies_arg_parser``
-- shared argparse parent parsers for the ``BLUEPRINT`` positional and the
``-D`` flag
"""

from argparse import ArgumentParser

__all__ = ("build_blueprint_arg_parser", "build_no_dependencies_arg_parser")


# Public API  ##################################################################
def build_blueprint_arg_parser(*, is_render_profile=False):
    """
    :param is_render_profile: whether the command takes the render
            profile options, appending ``v.s.`` to the help
    :type is_render_profile: bool
    :return: a fresh, help-suppressed parent parser carrying the optional
            ``BLUEPRINT`` positional: a registered name, or stdin when
            omitted
    :rtype: ArgumentParser
    """
    parent = ArgumentParser(add_help=False)
    parent.add_argument(
        "BLUEPRINT",
        help="registered blueprint name; omitted reads stdin"
        + (", v.s." if is_render_profile else ""),
        type=str,
        nargs="?",
        default=None,
    )

    return parent


def build_no_dependencies_arg_parser():
    """
    :return: a fresh, help-suppressed parent parser carrying ``-D``
    :rtype: ArgumentParser
    """
    parent = ArgumentParser(add_help=False)
    parent.add_argument(
        "-D",
        "--no-dependencies",
        dest="is_no_dependencies",
        action="store_true",
        default=False,
        help="use the blueprint's own nodes only, dependencies left out",
    )

    return parent
