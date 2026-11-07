"""build one consumer's plugin .zip as a GitHub Release asset"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

import kamilog
from kaye_engine import PACKAGE_NAME
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude import CLAUDE_DOC_DESCRIPTION, LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.plugin.export_zip import export_plugin_as_zip
from kaye_engine.cli.claude.plugin_marketplace_name import (
    check_setup_for_claude_cli,
    select_plugin_consumers,
)
from kaye_engine.cli.dry_run import (
    apply_dry_run_arg,
    build_dry_run_parent_parser,
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

_DEFAULT_OUTPUT_FOLDER = Path("dist")

_DESCRIPTION = (
    __doc__
    + """

writes the one versioned plugin .zip of CONSUMER_PROJ, built as
'claude plugin -z' builds it, for a release workflow to attach to a GitHub
Release. Run it from a consumer's console script, which registers the
consumers: CONSUMER_CLI build-github-release CONSUMER_PROJ -o dist
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
        "consumer_proj",
        metavar="CONSUMER_PROJ",
        help="canonical name of the consumer to build",
    )

    github_release_parser.add_argument(
        "-o",
        "--output",
        metavar="FOLDER",
        type=Path,
        default=_DEFAULT_OUTPUT_FOLDER,
        help="destination folder for the .zip; default: dist/",
    )

    kamilog.add_verbose_arguments(github_release_parser)

    def _github_release_main(args):
        kamilog.set_logging_level_by_namespace(args, logger=logger)
        apply_dry_run_arg(args)
        logger.enter("{} build-github-release".format(PACKAGE_NAME))
        check_setup_for_claude_cli()

        try:
            (consumer,) = select_plugin_consumers(args.consumer_proj)
        except ValueError as err:
            logger.critical(str(err))
            raise SystemExit(1) from err

        render_profile = resolve_render_profile(
            args,
            default_show_comment=False,
        )
        export_plugin_as_zip(
            args.output,
            consumer,
            includes_version=True,
            render_profile=render_profile,
        )
        logger.done(
            "build github release asset:\t{}-{}.zip in {}".format(
                consumer.canonical_name, consumer.version, args.output
            )
        )

    github_release_parser.set_defaults(func=_github_release_main)
