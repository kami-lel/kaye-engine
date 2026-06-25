"""export as Claude Marketplace including a kaye plugin"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye import logger, kamilog

from .export import export_marketplace

# constants  ===================================================================

_DESCRIPTION = """

wrap the kaye plugin in a Claude marketplace: a marketplace.json manifest
alongside the full plugin nested under plugins/, ready to add and install.

MARKETPLACE/  (default: current directory)
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── kaye/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            ├── coder-python/
            │   └── SKILL.md
            └── ~~  (one folder per remaining skill)
"""


def register_parser(cli_subparser):  ####################################
    marketplace_parser = cli_subparser.add_parser(
        "marketplace",
        help=__doc__,
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
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

        logger.done("export marketplace:\t" + str(folder))

    marketplace_parser.set_defaults(func=_marketplace_main)
