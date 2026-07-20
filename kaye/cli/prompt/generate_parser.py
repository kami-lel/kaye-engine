"""
generate_parser.py

define ``register_generate_subparser``
"""

from kaye import logger, kamilog

from kaye.cli.prompt.blueprint_io_parser import blueprint_io_parser

# constants  ###################################################################
_HELP = "generate concrete prompt from blueprint"


_DESCRIPTION = _HELP + """

more description"""


def _generate_main(args):  ####################################################
    kamilog.set_logging_level_by_namespace(args, logger=logger)
    # todo: create blueprint from args, render prompt, write to
    # args.target_file or print it
    logger.error("kaye prompt generate: not implemented yet")
    raise NotImplementedError


def register_generate_subparser(cli_subparser):  ###############################
    """
    register the ``kaye prompt generate`` subcommand parser
    """
    generate_parser = cli_subparser.add_parser(
        "generate",
        help=_HELP,
        description=_DESCRIPTION,
        aliases=["gen"],
        parents=[blueprint_io_parser],
    )

    kamilog.add_verbose_arguments(generate_parser)

    generate_parser.set_defaults(func=_generate_main)
