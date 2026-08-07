"""
sparseness_parser.py

define ``sparseness_parser`` and ``SPARSENESS_DESCRIPTION`` -- the
``-s/--sparseness`` argument shared by any subcommand that calls
``PromptBlueprint.generate_prompt(sparseness=...)``
"""

from argparse import ArgumentParser, ArgumentTypeError

__all__ = (
    "SPARSENESS_DESCRIPTION",
    "sparseness_parser",
)


# constants  ###################################################################
SPARSENESS_DESCRIPTION = """\
SPARSENESS:

- -1 collapses the whole output into a single line
- 0 removes all blank lines
- 1 collapses every run of blank lines to a single blank line (default)
- 2 caps runs at two blank lines, and so on
- 〃
- 99 disables trimming entirely"""


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


# defining the arg shared by any subcommand calling generate_prompt(...)
sparseness_parser = ArgumentParser(add_help=False)
sparseness_parser.add_argument(
    "-s",
    "--sparseness",
    metavar="SPARSENESS",
    type=_sparseness_type,
    default=1,
    help="blank-line policy for the rendered prompt, v.s.",
)
