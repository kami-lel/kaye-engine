"""export all exportables as Agent Skills for Codex"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

import kamilog
from kaye_engine import PACKAGE_NAME
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.codex import CODEX_DOC_DESCRIPTION, LOGGER_CODEX_NAME
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
from kaye_engine.cli.verbosity import apply_verbosity_arg
from kaye_engine.skill.export_folders import export_skills_as_folders

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CODEX_NAME)

# constants  ===================================================================

# the personal skills folder Codex reads across every repo
DEFAULT_CODEX_SKILLS_FOLDER = Path.home() / ".agents" / "skills"

_DESCRIPTION = (
    __doc__
    + """

writes one SKILL.md per exportable as its own skill folder.

FOLDER/  (default: ~/.agents/skills/)
├── coder-python/
│   └── SKILL.md
└── ~~  (one folder per remaining exportable)
"""
    + CODEX_DOC_DESCRIPTION
    + RENDER_PROFILE_DESCRIPTION
    + """

render defaults: surface=codex, comment=False, sparseness=0
"""
)


# pylint: disable=missing-function-docstring
def register_codex_skills_parser(cli_subparser):  ##############################
    skills_parser = cli_subparser.add_parser(
        "skills",
        help=__doc__,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["s"],
        parents=[
            build_render_profile_parent_parser(
                default_surface=("codex",),
                default_sparseness=DEFAULT_SPARSENESS,
            ),
            build_dry_run_parent_parser(),
        ],
    )

    skills_parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=DEFAULT_CODEX_SKILLS_FOLDER,
        help="destination folder; default: ~/.agents/skills/",
    )

    kamilog.add_verbose_arguments(skills_parser)

    def _skills_main(args):
        apply_verbosity_arg(args)
        apply_dry_run_arg(args)
        logger.enter("{} codex skills".format(PACKAGE_NAME))
        check_corpus_setup_for_cli()

        render_profile = resolve_render_profile(
            args,
            default_show_comment=False,
        )
        export_skills_as_folders(args.folder, render_profile=render_profile)
        logger.done("export skills as folders\t" + str(args.folder))

    skills_parser.set_defaults(func=_skills_main)
