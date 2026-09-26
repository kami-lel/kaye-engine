"""export each exportable as a Continue rule or prompt"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye_engine import PACKAGE_NAME, kamilog
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude.setup import get_surface_profiles
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.continue_ai import LOGGER_CONTINUE_NAME
from kaye_engine.cli.continue_ai.export_rules import export_continue_folder
from kaye_engine.cli.render_profile_parser import (
    build_render_profile_parent_parser,
    resolve_render_profile,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CONTINUE_NAME)

# constants  ===================================================================

_DEFAULT_CONTINUE_FOLDER = Path.home() / ".continue"

_DESCRIPTION = """

writes one .md per exportable, as a rule or as a prompt;
always-apply and LLM-invokable entries are rules,
other user-invokable entries are prompts.

FOLDER/  (default: ~/.continue/)
├── rules/
│   └── coder-python.md
└── prompts/
    └── ~~  (one file per prompt)
"""


# pylint: disable=missing-function-docstring
def register_continue_parser(cli_subparser):  ##################################
    continue_parser = cli_subparser.add_parser(
        "continue",
        help=__doc__,
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["c"],
        parents=[
            build_render_profile_parent_parser(
                default_surface=(),
                default_sparseness=DEFAULT_SPARSENESS,
                surface_profiles=get_surface_profiles(),
            )
        ],
    )

    continue_parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=_DEFAULT_CONTINUE_FOLDER,
        help="Continue config folder; default: ~/.continue/",
    )

    kamilog.add_verbose_arguments(continue_parser)

    def _continue_main(args):
        kamilog.set_logging_level_by_namespace(args, logger=logger)
        logger.enter("{} continue".format(PACKAGE_NAME))
        check_corpus_setup_for_cli()

        render_profile = resolve_render_profile(
            args,
            surface_profiles=get_surface_profiles(),
            default_show_comment=False,
        )
        export_continue_folder(args.folder, render_profile=render_profile)

        logger.done("export Continue rules & prompts\t" + str(args.folder))

    continue_parser.set_defaults(func=_continue_main)
