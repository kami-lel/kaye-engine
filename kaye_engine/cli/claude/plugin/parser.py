"""export all exportable as a single Claude plugin"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye_engine import PACKAGE_NAME, kamilog
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.plugin_marketplace_name import (
    check_setup_for_claude_cli,
)
from kaye_engine.cli.render_options_parser import (
    build_render_options_parent_parser,
    resolve_render_options,
)

from .export_folder import export_plugin_as_folder
from .export_zip import export_plugin_as_zip

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ===================================================================

_DEFAULT_PLUGINS_FOLDER = Path.home() / ".claude" / "plugins"

_DESCRIPTION = """

writes plugin.json and one SKILL.md per exportable under PLUGIN_NAME/skills/;
with -z, creates an upload-ready .zip for
Claude Desktop instead.

FOLDER/  (default: ~/.claude/plugins/)
└── PLUGIN_NAME/
    ├── .claude-plugin/
    │   └── plugin.json
    └── skills/
        ├── coder-python/
        │   └── SKILL.md
        └── ~~  (one folder per remaining skill)
"""


# pylint: disable=missing-function-docstring
def register_plugin_parser(cli_subparser):  ####################################
    plugin_parser = cli_subparser.add_parser(
        "plugin",
        help=__doc__,
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["p"],
        parents=[
            build_render_options_parent_parser(
                default_surface=("vsc",),
                default_sparseness=DEFAULT_SPARSENESS,
            )
        ],
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
        logger.enter("{} claude plugin".format(PACKAGE_NAME))
        check_setup_for_claude_cli()

        folder = args.folder
        if folder is None:
            folder = Path.cwd() if args.zip else _DEFAULT_PLUGINS_FOLDER
        render_kwargs = resolve_render_options(
            args, default_show_comment=False
        )

        if args.zip:
            logger.debug("export plugin as zip")
            export_plugin_as_zip(
                folder,
                includes_version=args.includes_version,
                render_kwargs=render_kwargs,
            )
            done_msg = "export plugin as zip"
        else:
            logger.debug("export plugin as folder")
            export_plugin_as_folder(folder, render_kwargs=render_kwargs)
            done_msg = "export plugin as folder"

        logger.done(done_msg + "\t" + str(folder))

    plugin_parser.set_defaults(func=_plugin_main)
