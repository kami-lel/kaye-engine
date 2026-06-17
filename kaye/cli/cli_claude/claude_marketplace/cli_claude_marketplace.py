"""export as Claude Marketplace including a kaye plugin"""

from pathlib import Path

from kaye import logger, kamilog

from .export_marketplace import export_marketplace


def register_cli_claude_marketplace_parser(  ####################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    marketplace_parser = cli_subparser.add_parser(
        "marketplace",
        help=__doc__,
        description=__doc__,
        aliases=["m"],
    )

    marketplace_parser.add_argument(
        "folder",
        nargs="?",
        metavar="MARKETPLACE",
        type=Path,
        default=Path.cwd(),
        help="destination folder; default: current directory",
    )

    kamilog.add_verbose_arguments(marketplace_parser)

    def _marketplace_main(args):
        kamilog.set_logging_level_by_verbosity(args, logger=logger)
        logger.enter("kaye claude marketplace")

        folder = args.folder

        export_marketplace(folder)

        logger.done("export marketplace\t" + str(folder))

    marketplace_parser.set_defaults(func=_marketplace_main)
