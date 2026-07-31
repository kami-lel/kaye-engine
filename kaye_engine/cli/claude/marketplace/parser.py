"""package the kaye plugin as an installable Claude marketplace"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye_engine import logger, kamilog

from .export import export_marketplace

# Bug exported folder structure contains name: kaye-engine


# constants  ===================================================================

_DESCRIPTION = """

writes marketplace.json and exports the kaye plugin into plugins/; the
resulting folder can be added directly in Claude's marketplace settings.

MARKETPLACE/  (default: ~/.claude/kaye_marketplace)
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── kaye-engine/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            ├── coder-python/
            │   └── SKILL.md
            └── ~~  (one folder per remaining skill)
"""


# pylint: disable=missing-function-docstring
def register_marketplace_subparser(cli_subparser):  ############################
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
        default=Path.home() / ".claude" / "kaye_marketplace",
        help="destination folder; default: ~/.claude/kaye_marketplace",
    )

    kamilog.add_verbose_arguments(marketplace_parser)

    def _marketplace_main(args):
        kamilog.set_logging_level_by_namespace(args, logger=logger)
        # FIXME retired program name reaches verbose output; use kaye-engine
        logger.enter("kaye claude marketplace")

        folder = args.folder

        export_marketplace(folder)

        logger.done("export marketplace:\t" + str(folder))

    marketplace_parser.set_defaults(func=_marketplace_main)
