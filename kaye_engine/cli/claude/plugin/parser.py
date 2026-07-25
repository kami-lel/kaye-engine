"""export all kaye blueprints as a single Claude plugin"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path


from kaye_engine import logger, kamilog

from .export_folder import export_plugin_as_folder
from .export_zip import export_plugin_as_zip

# constants  ===================================================================

_DEFAULT_PLUGINS_FOLDER = Path.home() / ".claude" / "plugins"

_DESCRIPTION = """

writes plugin.json and one SKILL.md per blueprint under kaye/skills/; with
-z, creates an upload-ready .zip for Claude Desktop instead.

FOLDER/  (default: ~/.claude/plugins/)
└── kaye/
    ├── .claude-plugin/
    │   └── plugin.json
    └── skills/
        ├── coder-python/
        │   └── SKILL.md
        └── ~~  (one folder per remaining skill)
"""


# pylint: disable=missing-function-docstring
def register_plugin_subparser(cli_subparser):  #################################
    plugin_parser = cli_subparser.add_parser(
        "plugin",
        help=__doc__,
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["p"],
    )

    plugin_parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=None,
        help="destination folder; default: ~/.claude/plugins/",
    )

    plugin_parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        dest="zip",
        help=(
            "create an upload-ready .zip plugin (for Claude Desktop); "
            "FOLDER default: current directory"
        ),
    )

    plugin_parser.add_argument(
        "-n",
        "--no-version",
        action="store_false",
        dest="includes_version",
        help="omit the current version from the .zip filename (zip only)",
    )

    kamilog.add_verbose_arguments(plugin_parser)

    def _plugin_main(args):
        kamilog.set_logging_level_by_namespace(args, logger=logger)
        logger.enter("kaye claude plugin")

        folder = args.folder
        if folder is None:
            folder = Path.cwd() if args.zip else _DEFAULT_PLUGINS_FOLDER

        if args.zip:
            logger.debug("export plugin as zip")
            export_plugin_as_zip(folder, includes_version=args.includes_version)
            done_msg = "export plugin as zip"
        else:
            logger.debug("export plugin as folder")
            export_plugin_as_folder(folder)
            done_msg = "export plugin as folder"

        logger.done(done_msg + "\t" + str(folder))

    plugin_parser.set_defaults(func=_plugin_main)
