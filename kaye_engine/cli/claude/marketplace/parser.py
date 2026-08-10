"""package the kaye plugin as an installable Claude marketplace"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye_engine import PACKAGE_NAME, kamilog
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.plugin_marketplace_name import (
    check_setup_for_claude_cli,
)
from kaye_engine.cli.claude.setup import get_marketplace_folder_name

from .export import export_marketplace

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ===================================================================

_DESCRIPTION = """

writes marketplace.json and exports into plugins/;
the resulting folder can be added directly in Claude's marketplace settings.

MARKETPLACE/  (default: ~/.claude/MARKETPLACE_FOLDER_NAME)
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── PLUGIN_NAME/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            ├── coder-python/
            │   └── SKILL.md
            └── ~~  (one folder per remaining skill)
"""


# pylint: disable=missing-function-docstring
def register_marketplace_parser(cli_subparser):  ###############################
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
        default=None,
        help="destination folder; default: ~/.claude/<marketplace folder>",
    )

    kamilog.add_verbose_arguments(marketplace_parser)

    def _marketplace_main(args):
        kamilog.set_logging_level_by_namespace(args, logger=logger)
        logger.enter("{} claude marketplace".format(PACKAGE_NAME))
        check_setup_for_claude_cli()

        folder = args.folder
        if folder is None:
            folder = Path.home() / ".claude" / get_marketplace_folder_name()

        export_marketplace(folder)

        logger.done("export marketplace:\t" + str(folder))

    marketplace_parser.set_defaults(func=_marketplace_main)
