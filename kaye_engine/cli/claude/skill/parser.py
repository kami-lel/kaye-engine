"""export each exportable as an individual Claude skill"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

from kaye_engine import PACKAGE_NAME, kamilog
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.setup import get_claude_cli_consumer_version
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.render_options_parser import (
    build_render_options_parent_parser,
    resolve_render_options,
)

from .export_folders import (
    export_skills_as_folders,
)
from .export_zips import export_skills_as_zips

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
def register_skill_parser(cli_subparser):  #####################################
    skill_parser = cli_subparser.add_parser(
        "skill",
        help=__doc__,
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["s"],
        parents=[
            build_render_options_parent_parser(
                default_surface=("chat",),
                default_sparseness=DEFAULT_SPARSENESS,
            )
        ],
    )

    skill_parser.add_argument(
        "folder",
        nargs="?",
        metavar="FOLDER",
        type=Path,
        default=None,
        help="destination folder; default: ~/.claude/skills/",
    )

    skill_parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        dest="zip",
        help="create .zip Skill packages; FOLDER default: current directory",
    )

    kamilog.add_verbose_arguments(skill_parser)

    def _skill_main(args):
        kamilog.set_logging_level_by_namespace(args, logger=logger)
        logger.enter("{} claude skill".format(PACKAGE_NAME))
        check_corpus_setup_for_cli()

        folder = args.folder
        if folder is None:
            folder = Path.cwd() if args.zip else _DEFAULT_SKILLS_FOLDER
        render_kwargs = resolve_render_options(
            args, default_show_comment=False
        )

        if args.zip:
            logger.debug("export skills as zip packages")
            export_skills_as_zips(folder, render_kwargs=render_kwargs)
            done_msg = "export skills as zip packages"
        else:
            logger.debug("export skills as folders")
            export_skills_as_folders(
                folder,
                version=get_claude_cli_consumer_version(),
                render_kwargs=render_kwargs,
            )
            done_msg = "export skills as folders"

        logger.done(done_msg + "\t" + str(folder))

    skill_parser.set_defaults(func=_skill_main)
