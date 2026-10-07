"""
sparseness_parser.py

define ``build_sparseness_parent_parser`` -- the ``-s/--sparseness``
argument shared by any subcommand that calls
``render_prompt(blueprint, profile=RenderProfile(sparseness=...))``
"""

from argparse import ArgumentParser, ArgumentTypeError

from kaye_engine.cli import DEFAULT_SPARSENESS

__all__ = (
    "build_sparseness_parent_parser",
)


# auxiliaries  #################################################################
def _sparseness_type(value):
    """
    argparse ``type`` for ``--sparseness``: an int, or the literal
    string ``"none"`` (case-insensitive) mapped to ``None``
    """
    if value.lower() == "none":
        return None

    try:
        return int(value)
    except ValueError as err:
        raise ArgumentTypeError(
            "sparseness must be an integer or 'none': {!r}".format(value)
        ) from err


# Main Entry Point  ############################################################
def build_sparseness_parent_parser(default=DEFAULT_SPARSENESS):
    """
    build a fresh, help-suppressed ``ArgumentParser`` carrying only the
    ``-s/--sparseness`` flag, for use as a `parents=[...]` entry -- a
    fresh instance per call avoids `parents=` option-string conflicts
    across the several subcommands sharing this builder


    :param default: sparseness value used when ``--sparseness`` is
            omitted
    :type default: int or None
    :return: the parent parser
    :rtype: ArgumentParser
    """
    parent = ArgumentParser(add_help=False)
    parent.add_argument(
        "-s",
        "--sparseness",
        metavar="SPARSENESS",
        type=_sparseness_type,
        default=default,
        help="blank-line policy for the rendered prompt, v.s.",
    )
    return parent
