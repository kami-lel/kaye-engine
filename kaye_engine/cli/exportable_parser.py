"""
exportable_parser.py

define ``register_exportable_parser``
"""

from argparse import RawDescriptionHelpFormatter

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.render_options_parser import (
    build_render_options_parent_parser,
    resolve_render_options,
)
from kaye_engine.exportable import exportable_registry
from kaye_engine.kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
_HELP = "print an exportable's content, or list all exportables"

_DESCRIPTION = _HELP + """

prints the content of the exportable registered under EXPORTABLE:

    kaye-engine exportable my-canonical-name

list every registered exportable, sorted alphabetically:

    kaye-engine exportable ls
"""


# auxiliaries  #################################################################
def _exportable_main(args):
    set_logging_level_by_namespace(args, logger=logger)
    check_corpus_setup_for_cli()

    if args.EXPORTABLE == "ls":
        for name in sorted(exportable_registry):
            print(name)
        return

    try:
        exportable = exportable_registry[args.EXPORTABLE]
    except KeyError as err:
        logger.critical("unknown exportable:\t" + args.EXPORTABLE)
        raise SystemExit(1) from err

    render_kwargs = resolve_render_options(args, default_show_comment=False)
    print(exportable.content(**render_kwargs))


# Public API  ##################################################################
def register_exportable_parser(cli_subparser):
    """
    register the ``kaye-engine exportable`` subcommand parser
    """
    export_parser = cli_subparser.add_parser(
        "exportable",
        help=_HELP,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["x"],
        parents=[
            build_render_options_parent_parser(
                default_sparseness=DEFAULT_SPARSENESS
            )
        ],
    )

    # add arguments  -------------------------------------------------------
    export_parser.add_argument(
        "EXPORTABLE",
        help="exportable canonical name; EXPORTABLE=ls: list all exportables",
    )
    add_verbose_arguments(export_parser)

    export_parser.set_defaults(func=_exportable_main)
