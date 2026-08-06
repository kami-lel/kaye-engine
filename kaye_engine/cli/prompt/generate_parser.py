"""
generate_parser.py

define ``register_generate_parser``
"""

from argparse import ArgumentTypeError, RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)

from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.prompt.blueprint_io_parser import (
    blueprint_io_parser,
    load_blueprint_from_args,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# todo cli prompt generate: allow sidecars be arg

# constants  ###################################################################
_HELP = "generate concrete prompt from blueprint"


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


_DESCRIPTION = _HELP + """

renders blueprint into a final system prompt; the result is printed to stdout

select blueprint by registry name BLUEPRINT:

    kaye-engine prompt generate my-blueprint

reading blueprint from stdin:

    kaye-engine prompt generate < my-blueprint.yaml
    cat my-blueprint.yaml | kaye-engine prompt generate
"""


def _generate_main(args):  ####################################################
    set_logging_level_by_namespace(args, logger=logger)
    check_corpus_setup_for_cli()

    blueprint, display_name = load_blueprint_from_args(args)

    prompt = blueprint.generate_prompt(
        show_comment=not args.no_comment,
        display_name=display_name,
        sparseness=args.sparseness,
    )

    print(prompt)


def register_generate_parser(cli_subparser):  ##################################
    """
    register the ``kaye prompt generate`` subcommand parser
    """
    generate_parser = cli_subparser.add_parser(
        "generate",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["g"],
        parents=[blueprint_io_parser],
    )

    generate_parser.add_argument(
        "-s",
        "--sparseness",
        metavar="SPARSENESS",
        type=_sparseness_type,
        default=1,
        help=(
            "blank-line policy for the rendered prompt: 'none' disables "
            "trimming entirely, 0 removes all blank lines, 1 collapses "
            "every run of blank lines to a single blank line (default), "
            "2+ caps runs at that count, and -1 collapses the whole "
            "output into a single line"
        ),
    )

    add_verbose_arguments(generate_parser)

    generate_parser.set_defaults(func=_generate_main)
