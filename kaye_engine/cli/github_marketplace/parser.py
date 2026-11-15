"""build the GitHub marketplace repo of the consumer project"""

import copy
from argparse import RawDescriptionHelpFormatter
from pathlib import Path

import kamilog
from kaye_engine import LOGGER_NAME, PACKAGE_NAME
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.dry_run import (
    apply_dry_run_arg,
    build_dry_run_parent_parser,
)
from kaye_engine.cli.plugin_platform.consumers import (
    check_setup_for_plugin_cli,
    get_plugin_consumers,
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

from .export import (
    MARKETPLACE_PLATFORMS,
    export_github_marketplace,
    get_github_marketplace_name,
)

__all__ = ("register_github_marketplace_parser",)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME + ".github-marketplace")

# constants  ===================================================================

_DESCRIPTION = (
    __doc__
    + """

writes into OUTPUT a marketplace repo root that both Claude and Codex add
by URL, for a release workflow to push to the marketplace repo:

OUTPUT/
├── .claude-plugin/
│   └── marketplace.json      (Claude)
├── .agents/
│   └── plugins/
│       └── marketplace.json  (Codex)
└── plugins/
    ├── claude/PLUGIN_NAME/   (surface claude)
    └── codex/PLUGIN_NAME/    (surface codex)

the marketplace is named REPO-marketplace from the repo name the consumer
project registered, and lists every plugin consumer; only the 3 entries
above are written, so a README.md or any other root file stays untouched.
--surface is refused: each half renders its own surface. --dry-run lists
every write and writes nothing. Run it from a consumer's console script:
CONSUMER_CLI build-github-marketplace market
"""
    + RENDER_PROFILE_DESCRIPTION
    + """

render defaults: surface=claude & codex (one per half), comment=False,
sparseness=0
"""
)


def _resolve_platform_render_profiles(args):
    """
    :return: the render profile per platform name, each the shared render
            flags plus the platform's own default surface
    :rtype: dict[str, RenderProfile]
    """
    profiles = {}
    for platform, _plugins_dir in MARKETPLACE_PLATFORMS:
        platform_args = copy.copy(args)
        platform_args.surface = list(platform.default_surface)
        profiles[platform.name] = resolve_render_profile(
            platform_args, default_show_comment=False
        )
    return profiles


# pylint: disable=missing-function-docstring
def register_github_marketplace_parser(cli_subparser):  ########################
    marketplace_parser = cli_subparser.add_parser(
        "build-github-marketplace",
        help=__doc__,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        parents=[
            build_render_profile_parent_parser(
                default_sparseness=DEFAULT_SPARSENESS,
            ),
            build_dry_run_parent_parser(),
        ],
    )

    marketplace_parser.add_argument(
        "output",
        metavar="OUTPUT",
        type=Path,
        help="the marketplace repo root to write, e.g. market",
    )

    kamilog.add_verbose_arguments(marketplace_parser)

    def _github_marketplace_main(args):
        apply_verbosity_arg(args)
        apply_dry_run_arg(args)
        logger.enter("{} build-github-marketplace".format(PACKAGE_NAME))
        check_setup_for_plugin_cli()

        if args.surface:
            logger.critical(
                "--surface is not taken: Claude plugins render for claude, "
                "Codex plugins for codex"
            )
            raise SystemExit(1)

        # every name first: an unset registry exits 1 before any write
        name = get_github_marketplace_name()
        owner = get_default_consumer().canonical_name
        consumers = get_plugin_consumers()
        if not consumers:
            logger.critical("no plugin consumer holds an exportable")
            raise SystemExit(1)

        paths = export_github_marketplace(
            args.output, owner, _resolve_platform_render_profiles(args)
        )
        logger.done(
            "build github marketplace {} in {}:\n{}".format(
                name,
                args.output,
                "\n".join(str(path) for path in paths),
            )
        )

    marketplace_parser.set_defaults(func=_github_marketplace_main)
