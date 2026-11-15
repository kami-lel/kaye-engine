"""build the GitHub Release assets of the consumer project"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

import kamilog
from kaye_engine.cli.verbosity import apply_verbosity_arg
from kaye_engine import PACKAGE_NAME
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude import CLAUDE_DOC_DESCRIPTION, LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.plugin.export_zip import export_plugin_as_zip
from kaye_engine.cli.claude.plugin_marketplace_name import (
    check_setup_for_claude_cli,
    get_plugin_consumers,
)
from kaye_engine.cli.dry_run import (
    apply_dry_run_arg,
    build_dry_run_parent_parser,
)
from kaye_engine.cli.github_release.asset_name import (
    ASSET_DESKTOP_PLUGIN,
    get_release_asset_name,
    get_release_asset_stem,
)
from kaye_engine.cli.render_profile_description import (
    RENDER_PROFILE_DESCRIPTION,
)
from kaye_engine.cli.render_profile_parser import (
    build_render_profile_parent_parser,
    resolve_render_profile,
)

__all__ = ("register_github_release_parser",)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ===================================================================

_DESCRIPTION = (
    __doc__
    + """

writes into OUTPUT one Claude Desktop plugin .zip per plugin consumer,
built as 'claude plugin -z' builds it, for a release workflow to attach to
a GitHub Release. Each file is named REPO-VERSION-TYPE[-CONSUMER].zip from
the repo name and version the consumer project registered; the default
consumer's name is left out. Run it from a consumer's console script, which
registers them: CONSUMER_CLI build-github-release dist
"""
    + CLAUDE_DOC_DESCRIPTION
    + RENDER_PROFILE_DESCRIPTION
    + """

render defaults: surface=claude, comment=False, sparseness=0
"""
)


# pylint: disable=missing-function-docstring
def register_github_release_parser(cli_subparser):  ############################
    github_release_parser = cli_subparser.add_parser(
        "build-github-release",
        help=__doc__,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        parents=[
            build_render_profile_parent_parser(
                default_surface=("claude",),
                default_sparseness=DEFAULT_SPARSENESS,
            ),
            build_dry_run_parent_parser(),
        ],
    )

    github_release_parser.add_argument(
        "output",
        metavar="OUTPUT",
        type=Path,
        help="destination folder for the release assets, e.g. dist",
    )

    kamilog.add_verbose_arguments(github_release_parser)

    def _github_release_main(args):
        apply_verbosity_arg(args)
        apply_dry_run_arg(args)
        logger.enter("{} build-github-release".format(PACKAGE_NAME))
        check_setup_for_claude_cli()

        render_profile = resolve_render_profile(
            args,
            default_show_comment=False,
        )

        # every name first: an unset registry exits 1 before any write
        plugins = [
            (
                consumer,
                get_release_asset_name(
                    ASSET_DESKTOP_PLUGIN, consumer=consumer.canonical_name
                ),
            )
            for consumer in get_plugin_consumers()
        ]
        if not plugins:
            logger.critical("no plugin consumer holds an exportable")
            raise SystemExit(1)

        for consumer, _name in plugins:
            export_plugin_as_zip(
                args.output,
                consumer,
                render_profile=render_profile,
                zip_stem=lambda c: get_release_asset_stem(
                    ASSET_DESKTOP_PLUGIN, consumer=c.canonical_name
                ),
            )
        logger.done(
            "build github release assets in {}:\n{}".format(
                args.output, "\n".join(name for _c, name in plugins)
            )
        )

    github_release_parser.set_defaults(func=_github_release_main)
