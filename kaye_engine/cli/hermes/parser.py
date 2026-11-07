"""support Hermes Agent/Desktop"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

import kamilog
from kaye_engine.cli.verbosity import apply_verbosity_arg
from kaye_engine import PACKAGE_NAME
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.dry_run import (
    apply_dry_run_arg,
    build_dry_run_parent_parser,
)
from kaye_engine.cli.hermes import HERMES_DOC_DESCRIPTION, LOGGER_HERMES_NAME
from kaye_engine.cli.hermes.export import export_hermes_folder
from kaye_engine.cli.render_profile_description import (
    RENDER_PROFILE_DESCRIPTION,
)
from kaye_engine.cli.render_profile_parser import (
    build_render_profile_parent_parser,
    resolve_render_profile,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_HERMES_NAME)

# constants  ===================================================================

_DESCRIPTION = (
    __doc__ + """

write persona and skills into Hermes home directory:

FOLDER/  (the Hermes home directory)
├── SOUL.md
├── skills/
│   └── <consumer name>/<skill name>/SKILL.md
└── profiles/
    └── <profile name>/SOUL.md
"""
    + HERMES_DOC_DESCRIPTION
    + RENDER_PROFILE_DESCRIPTION
    + """

render defaults: surface=hermes, comment=False, sparseness=0
"""
)


# pylint: disable=missing-function-docstring
def register_hermes_parser(cli_subparser):  ####################################
    hermes_parser = cli_subparser.add_parser(
        "hermes",
        help=__doc__,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["m"],
        parents=[
            build_render_profile_parent_parser(
                default_surface=("hermes",),
                default_sparseness=DEFAULT_SPARSENESS,
            ),
            build_dry_run_parent_parser(),
        ],
    )

    hermes_parser.add_argument(
        "folder",
        metavar="FOLDER",
        type=Path,
        help="Hermes home directory",
    )

    kamilog.add_verbose_arguments(hermes_parser)

    def _hermes_main(args):
        apply_verbosity_arg(args)
        apply_dry_run_arg(args)
        logger.enter("{} hermes".format(PACKAGE_NAME))
        check_corpus_setup_for_cli()

        render_profile = resolve_render_profile(
            args,
            default_show_comment=False,
        )
        export_hermes_folder(
            args.folder, render_profile=render_profile
        )

        logger.done("export Hermes home directory\t" + str(args.folder))

    hermes_parser.set_defaults(func=_hermes_main)
