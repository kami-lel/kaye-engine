"""export each consumer's exportables as its own Claude plugin"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

import kamilog
from kaye_engine.cli.verbosity import apply_verbosity_arg
from kaye_engine import PACKAGE_NAME
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.plugin_marketplace_name import (
    check_setup_for_claude_cli,
)
from kaye_engine.cli.dry_run import (
    apply_dry_run_arg,
    build_dry_run_parent_parser,
)
from kaye_engine.cli.claude import CLAUDE_DOC_DESCRIPTION
from kaye_engine.cli.render_profile_description import (
    RENDER_PROFILE_DESCRIPTION,
)
from kaye_engine.cli.render_profile_parser import (
    build_render_profile_parent_parser,
    resolve_render_profile,
)

from .export_folder import export_plugins_as_folders
from .export_zip import export_plugins_as_zips

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ===================================================================

_DEFAULT_PLUGINS_FOLDER = Path.home() / ".claude" / "plugins"

_DESCRIPTION = (
    __doc__ + """

writes, per consumer, plugin.json and one SKILL.md per exportable of that
consumer under PLUGIN_NAME/skills/; with -z, creates one upload-ready .zip
(PLUGIN_NAME-claude-VERSION.zip) per consumer for Claude Desktop instead. CONSUMER_PROJ keeps only the
consumer of that name; naming it needs FOLDER first (plugin -z . NAME).

FOLDER/  (default: ~/.claude/plugins/)
└── PLUGIN_NAME/
    ├── .claude-plugin/
    │   └── plugin.json
    └── skills/
        ├── coder-python/
        │   └── SKILL.md
        └── ~~  (one folder per remaining skill)
"""
    + CLAUDE_DOC_DESCRIPTION
    + RENDER_PROFILE_DESCRIPTION
    + """

render defaults: surface=claude, comment=False, sparseness=0
"""
)


# pylint: disable=missing-function-docstring
def register_plugin_parser(cli_subparser):  ####################################
    plugin_parser = cli_subparser.add_parser(
        "plugin",
        help=__doc__,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["p"],
        parents=[
            build_render_profile_parent_parser(
                default_surface=("claude",),
                default_sparseness=DEFAULT_SPARSENESS,
            ),
            build_dry_run_parent_parser(),
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
        "consumer_proj",
        nargs="?",
        metavar="CONSUMER_PROJ",
        default=None,
        help="export only this consumer's plugin; default: every consumer",
    )

    plugin_parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        dest="zip",
        help=(
            "create upload-ready .zip plugins, 1 per consumer (for Claude Desktop); "
            "FOLDER default: current directory"
        ),
    )

    plugin_parser.add_argument(
        "-N",
        "--no-version",
        action="store_false",
        dest="includes_version",
        help="omit each version from the .zip filename (zip only)",
    )

    kamilog.add_verbose_arguments(plugin_parser)

    def _plugin_main(args):
        apply_verbosity_arg(args)
        apply_dry_run_arg(args)
        logger.enter("{} claude plugin".format(PACKAGE_NAME))
        check_setup_for_claude_cli()

        folder = args.folder
        if folder is None:
            folder = Path.cwd() if args.zip else _DEFAULT_PLUGINS_FOLDER
        render_profile = resolve_render_profile(
            args,
            default_show_comment=False,
        )

        if args.zip:
            logger.debug("export plugin as zip")
            try:
                count = export_plugins_as_zips(
                    folder,
                    includes_version=args.includes_version,
                    render_profile=render_profile,
                    consumer_name=args.consumer_proj,
                )
            except ValueError as err:
                logger.critical(str(err))
                raise SystemExit(1) from err
            logger.done("export plugin as {} zips".format(count))
        else:
            logger.debug("export plugin as folder")
            try:
                export_plugins_as_folders(
                    folder,
                    render_profile=render_profile,
                    consumer_name=args.consumer_proj,
                )
            except ValueError as err:
                logger.critical(str(err))
                raise SystemExit(1) from err
            logger.done("export plugin as folder\t" + str(folder))

    plugin_parser.set_defaults(func=_plugin_main)
