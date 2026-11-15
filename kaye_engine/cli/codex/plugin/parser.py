"""export each consumer's exportables as its own Codex plugin"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

import kamilog
from kaye_engine import PACKAGE_NAME
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.codex import CODEX_DOC_DESCRIPTION, LOGGER_CODEX_NAME
from kaye_engine.cli.dry_run import (
    apply_dry_run_arg,
    build_dry_run_parent_parser,
)
from kaye_engine.cli.plugin_platform.consumers import (
    check_setup_for_plugin_cli,
)
from kaye_engine.cli.render_profile_description import (
    RENDER_PROFILE_DESCRIPTION,
)
from kaye_engine.cli.render_profile_parser import (
    build_render_profile_parent_parser,
    resolve_render_profile,
)
from kaye_engine.cli.verbosity import apply_verbosity_arg
from kaye_engine.consumer import get_default_consumer

from .export import export_codex_plugins_as_folders

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CODEX_NAME)

# constants  ===================================================================

# the personal plugin folder of the Codex plugin-creator scaffold
DEFAULT_CODEX_PLUGINS_FOLDER = Path.home() / "plugins"

_DESCRIPTION = (
    __doc__
    + """

writes, per consumer, the portable plugin.json, the Codex
.codex-plugin/plugin.json, and one SKILL.md per exportable of that consumer
under PLUGIN_NAME/skills/. CONSUMER selects one consumer's plugin, default:
the default consumer the consumer project registered; naming it needs
FOLDER first (plugin . NAME).

FOLDER/  (default: ~/plugins/)
└── PLUGIN_NAME/
    ├── plugin.json
    ├── .codex-plugin/
    │   └── plugin.json
    └── skills/
        ├── coder-python/
        │   └── SKILL.md
        └── ~~  (one folder per remaining skill)
"""
    + CODEX_DOC_DESCRIPTION
    + RENDER_PROFILE_DESCRIPTION
    + """

render defaults: surface=codex, comment=False, sparseness=0
"""
)


# pylint: disable=missing-function-docstring
def register_codex_plugin_parser(cli_subparser):  ##############################
    plugin_parser = cli_subparser.add_parser(
        "plugin",
        help=__doc__,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["p"],
        parents=[
            build_render_profile_parent_parser(
                default_surface=("codex",),
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
        default=DEFAULT_CODEX_PLUGINS_FOLDER,
        help="destination folder; default: ~/plugins/",
    )

    plugin_parser.add_argument(
        "consumer",
        nargs="?",
        metavar="CONSUMER",
        default=None,
        help="export only this consumer's plugin; default: the default "
        "consumer of the consumer project",
    )

    kamilog.add_verbose_arguments(plugin_parser)

    def _plugin_main(args):
        apply_verbosity_arg(args)
        apply_dry_run_arg(args)
        logger.enter("{} codex plugin".format(PACKAGE_NAME))
        check_setup_for_plugin_cli()

        consumer_name = args.consumer
        if consumer_name is None:
            consumer_name = get_default_consumer().canonical_name
        render_profile = resolve_render_profile(
            args,
            default_show_comment=False,
        )

        try:
            export_codex_plugins_as_folders(
                args.folder,
                render_profile=render_profile,
                consumer_name=consumer_name,
            )
        except ValueError as err:
            logger.critical(str(err))
            raise SystemExit(1) from err
        logger.done("export codex plugin as folder\t" + str(args.folder))

    plugin_parser.set_defaults(func=_plugin_main)
