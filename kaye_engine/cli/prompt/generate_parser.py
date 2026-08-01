"""
generate_parser.py

define ``register_generate_parser``
"""

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.kamilog import add_verbose_arguments, set_logging_level_by_namespace

from kaye_engine.cli.prompt.blueprint_io_parser import (
    blueprint_io_parser,
    load_blueprint_from_args,
    write_blueprint_result,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# todo cli prompt generate: allow sidecars be arg

# constants  ###################################################################
_HELP = "generate concrete prompt from blueprint"


_DESCRIPTION = _HELP + """

renders BLUEPRINT into a final system prompt via generate_prompt(),
loading it from the registry by name or, with -f, parsing it from a
source file; the result is printed to stdout or, with -F, written to a
file"""


def _generate_main(args):  ####################################################
    set_logging_level_by_namespace(args, logger=logger)

    blueprint, display_name = load_blueprint_from_args(args)

    prompt = blueprint.generate_prompt(
        show_comment=not args.no_comment,
        display_name=display_name,
    )

    write_blueprint_result(prompt, args.target_file)


def register_generate_parser(cli_subparser):  ##################################
    """
    register the ``kaye prompt generate`` subcommand parser
    """
    generate_parser = cli_subparser.add_parser(
        "generate",
        help=_HELP,
        description=_DESCRIPTION,
        aliases=["g"],
        parents=[blueprint_io_parser],
    )

    add_verbose_arguments(generate_parser)

    generate_parser.set_defaults(func=_generate_main)
