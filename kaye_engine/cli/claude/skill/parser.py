"""export each kaye blueprint as an individual Claude skill"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path


from kaye_engine import logger, kamilog


from .export_folders import (
    export_skills_as_folders,
)
from .export_zips import export_skills_as_zips

# constants  ===================================================================

_DEFAULT_SKILLS_FOLDER = Path.home() / ".claude" / "skills"

_DESCRIPTION = """

writes one SKILL.md per blueprint, prompt, and abbreviation group as its own
skill folder; with -z, creates a .zip per skill instead.

FOLDER/  (default: ~/.claude/skills/)
├── coder-python/
│   └── SKILL.md
└── ~~  (one folder per remaining blueprint, prompt, and abbr group)
"""


# pylint: disable=missing-function-docstring
def register_skill_subparser(cli_subparser):  ##################################
    skill_parser = cli_subparser.add_parser(
        "skill",
        help=__doc__,
        description=__doc__ + _DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["s"],
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
        logger.enter("kaye claude skill")

        folder = args.folder
        if folder is None:
            folder = Path.cwd() if args.zip else _DEFAULT_SKILLS_FOLDER

        if args.zip:
            logger.debug("export skills as zip packages")
            export_skills_as_zips(folder)
            done_msg = "export skills as zip packages"
        else:
            logger.debug("export skills as folders")
            export_skills_as_folders(folder)
            done_msg = "export skills as folders"

        logger.done(done_msg + "\t" + str(folder))

    skill_parser.set_defaults(func=_skill_main)
