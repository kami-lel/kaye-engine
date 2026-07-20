"""
show_parser.py

define ``register_show_subparser``
"""

from kaye import logger, kamilog

from kaye.cli.prompt.blueprint_io_parser import blueprint_io_parser

# constants  ###################################################################

_HELP = "show content of any of embedded blueprints"


_DESCRIPTION = _HELP + """

more description"""


def _show_main(args):  #########################################################
    kamilog.set_logging_level_by_namespace(args, logger=logger)
    # TODO: create blueprint from args, render preview tree, write to
    # args.target_file or print it
    logger.error("kaye prompt show: not implemented yet")
    raise NotImplementedError


def register_show_subparser(cli_subparser):  ###################################
    """
    register the ``kaye prompt show`` subcommand parser
    """
    show_parser = cli_subparser.add_parser(
        "show",
        help=_HELP,
        description=_DESCRIPTION,
        parents=[blueprint_io_parser],
    )

    # add arguments  -----------------------------------------------------------
    # options
    show_parser.add_argument(
        "-l",
        "--preview-line-count",
        metavar="LINE_COUNT",
        type=int,
        nargs="?",
        help="maximum line count for each entry in blueprint preview",
        default=None,
    )
    show_parser.add_argument(
        "-w",
        "--preview-line-width",
        metavar="LINE_WIDTH",
        type=int,
        nargs="?",
        help="maximum line width for each entry in blueprint preview",
        default=None,
    )
    show_parser.add_argument(
        "-t",
        "--show-full-tree",
        action="store_true",
        help="display the entire preview tree",
    )

    kamilog.add_verbose_arguments(show_parser)

    show_parser.set_defaults(func=_show_main)
