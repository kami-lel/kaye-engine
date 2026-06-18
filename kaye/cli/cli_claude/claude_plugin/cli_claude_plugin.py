"""export as an Anthropic Claude plugin"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path


from kaye import logger, kamilog

from .export_plugin_as_folder import export_plugin_as_folder
from .export_plugin_as_zip import export_plugin_as_zip

# constants  ===================================================================

_DEFAULT_PLUGINS_FOLDER = Path.home() / ".claude" / "plugins"

_DESCRIPTION = """

bundle every blueprint, prompt, and abbreviation group into a single Claude
plugin folder (a plugin.json manifest plus one skills/ subfolder); with -z,
pack it as an upload-ready .zip plugin instead.

FOLDER/  (default: ~/.claude/plugins/)
└── kaye/  (plugin root)
    ├── .claude-plugin/
    │   └── plugin.json
    └── skills/
        ├── coder-python/
        │   └── SKILL.md
        └── ~~  (one folder per remaining skill)
"""


def register_cli_claude_plugin_parser(  ########################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
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
        kamilog.set_logging_level_by_verbosity(args, logger=logger)
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
