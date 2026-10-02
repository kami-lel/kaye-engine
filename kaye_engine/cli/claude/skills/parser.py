"""export all exportables as Agent Skills for Claude"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

import kamilog
from kaye_engine import PACKAGE_NAME
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude import CLAUDE_DOC_DESCRIPTION, LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.setup import get_surface_profiles
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.dry_run import (
    apply_dry_run_arg,
    build_dry_run_parent_parser,
)
from kaye_engine.cli.render_profile_parser import (
    RENDER_PROFILE_DESCRIPTION,
    build_render_profile_parent_parser,
    resolve_render_profile,
)
from kaye_engine.consumer import get_consumer_version
from kaye_engine.skill.export_folders import export_skills_as_folders
from kaye_engine.skill.export_zips import export_skills_as_zips

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ===================================================================

_DEFAULT_SKILLS_FOLDER = Path.home() / ".claude" / "skills"

_DESCRIPTION = """

writes one SKILL.md per exportable as its own skill folder;
with -z, creates a .zip per skill instead.

FOLDER/  (default: ~/.claude/skills/)
├── coder-python/
│   └── SKILL.md
└── ~~  (one folder per remaining exportable)
"""


# pylint: disable=missing-function-docstring
def register_skills_parser(cli_subparser):  ####################################
    skills_parser = cli_subparser.add_parser(
        "skills",
        help=__doc__,
        description=__doc__
        + _DESCRIPTION
        + CLAUDE_DOC_DESCRIPTION
        + RENDER_PROFILE_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["s"],
        parents=[
            build_render_profile_parent_parser(
                default_surface=("chat",),
                default_sparseness=DEFAULT_SPARSENESS,
                surface_profiles=get_surface_profiles(),
            ),
            build_dry_run_parent_parser(),
        ],
    )

    skills_parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=None,
        help="destination folder; default: ~/.claude/skills/, v.s.",
    )

    skills_parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        dest="zip",
        help="create .zip Skill packages; FOLDER default: current directory",
    )

    kamilog.add_verbose_arguments(skills_parser)

    def _skills_main(args):
        kamilog.set_logging_level_by_namespace(args, logger=logger)
        apply_dry_run_arg(args)
        logger.enter("{} claude skills".format(PACKAGE_NAME))
        check_corpus_setup_for_cli()

        folder = args.folder
        if folder is None:
            folder = Path.cwd() if args.zip else _DEFAULT_SKILLS_FOLDER
        render_profile = resolve_render_profile(
            args,
            surface_profiles=get_surface_profiles(),
            default_show_comment=False,
        )
        version = get_consumer_version()

        if args.zip:
            logger.debug("export skills as zip packages")
            export_skills_as_zips(
                folder, version=version, render_profile=render_profile
            )
            done_msg = "export skills as zip packages"
        else:
            logger.debug("export skills as folders")
            export_skills_as_folders(
                folder, version=version, render_profile=render_profile
            )
            done_msg = "export skills as folders"

        logger.done(done_msg + "\t" + str(folder))

    skills_parser.set_defaults(func=_skills_main)
