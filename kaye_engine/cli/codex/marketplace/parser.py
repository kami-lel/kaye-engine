"""package every plugin as a Codex marketplace"""

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

from .export import export_codex_marketplace

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CODEX_NAME)

# constants  ===================================================================

# the personal marketplace root: ~/.agents/plugins/marketplace.json
DEFAULT_CODEX_MARKETPLACE_ROOT = Path.home()

_DESCRIPTION = (
    __doc__
    + """

writes .agents/plugins/marketplace.json and exports every consumer's plugin
into plugins/; the default ROOT, your home folder, is the personal
marketplace Codex reads; any other ROOT can be added with
'codex plugin marketplace add ROOT'.

ROOT/  (default: ~)
├── .agents/
│   └── plugins/
│       └── marketplace.json
└── plugins/
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
def register_codex_marketplace_parser(cli_subparser):  #########################
    marketplace_parser = cli_subparser.add_parser(
        "marketplace",
        help=__doc__,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["m"],
        parents=[
            build_render_profile_parent_parser(
                default_surface=("codex",),
                default_sparseness=DEFAULT_SPARSENESS,
            ),
            build_dry_run_parent_parser(),
        ],
    )

    marketplace_parser.add_argument(
        "root",
        nargs="?",
        metavar="ROOT",
        type=Path,
        default=DEFAULT_CODEX_MARKETPLACE_ROOT,
        help="marketplace root; default: ~ (the personal marketplace)",
    )

    kamilog.add_verbose_arguments(marketplace_parser)

    def _marketplace_main(args):
        apply_verbosity_arg(args)
        apply_dry_run_arg(args)
        logger.enter("{} codex marketplace".format(PACKAGE_NAME))
        check_setup_for_plugin_cli()

        render_profile = resolve_render_profile(
            args,
            default_show_comment=False,
        )
        path = export_codex_marketplace(
            args.root, render_profile=render_profile
        )
        logger.done("export codex marketplace\t" + str(path))

    marketplace_parser.set_defaults(func=_marketplace_main)
