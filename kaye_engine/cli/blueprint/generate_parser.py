"""
generate_parser.py

define ``register_generate_parser``
"""

from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)

from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.blueprint.blueprint_io_parser import (
    blueprint_io_parser,
    load_blueprint_from_args,
)
from kaye_engine.cli.sparseness_parser import (
    SPARSENESS_DESCRIPTION,
    sparseness_parser,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# todo cli prompt generate: allow sidecars be arg

# constants  ###################################################################
_HELP = "generate concrete prompt from blueprint"

_DESCRIPTION = _HELP + """

renders blueprint into a final system prompt; the result is printed to stdout

select blueprint by registry name BLUEPRINT:

    kaye-engine blueprint generate my-blueprint

reading blueprint from stdin:

    kaye-engine blueprint generate < my-blueprint.yaml
    cat my-blueprint.yaml | kaye-engine blueprint generate

""" + SPARSENESS_DESCRIPTION


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
    register the ``kaye blueprint generate`` subcommand parser
    """
    generate_parser = cli_subparser.add_parser(
        "generate",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["gen", "g"],
        parents=[blueprint_io_parser, sparseness_parser],
    )

    add_verbose_arguments(generate_parser)

    generate_parser.set_defaults(func=_generate_main)
