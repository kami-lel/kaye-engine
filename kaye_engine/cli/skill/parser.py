"""export exportables as Agent Skills"""

from argparse import RawDescriptionHelpFormatter
from pathlib import Path

import kamilog
from kaye_engine import PACKAGE_NAME
from kaye_engine.cli import DEFAULT_SPARSENESS
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
from kaye_engine.skill import LOGGER_SKILL_NAME
from kaye_engine.skill.export_folders import export_skills_as_folders
from kaye_engine.skill.export_zips import export_skills_as_zips
from kaye_engine.skill.select import select_exportables

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_SKILL_NAME)

# constants  ===================================================================

_USAGE = """%(prog)s [-h] [-z] [-n] [NAME ...] FOLDER
       %(prog)s [-h] [-z] [-n] --all FOLDER"""

_DESCRIPTION = """

writes one SKILL.md per named skill as its own skill folder
by name or all, into a given FOLDER

FOLDER/
├── coder-python/
│   └── SKILL.md
└── ~~  (one folder per remaining NAME)
"""


# pylint: disable=missing-function-docstring
def register_skill_parser(cli_subparser):  #####################################
    skill_parser = cli_subparser.add_parser(
        "skill",
        help=__doc__,
        usage=_USAGE,
        description=__doc__ + _DESCRIPTION + RENDER_PROFILE_DESCRIPTION,
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

    # NAMEs and FOLDER share one positional: FOLDER is always the last
    skill_parser.add_argument(
        "paths",
        nargs="+",
        metavar="NAME... FOLDER",
        help="skill names to export, then the destination folder, v.s.",
    )

    skill_parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="is_all",
        help="export every skill; then only FOLDER is given",
    )

    skill_parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        dest="zip",
        help="create .zip Skill packages instead of folders",
    )

    kamilog.add_verbose_arguments(skill_parser)

    def _skill_main(args):
        kamilog.set_logging_level_by_namespace(args, logger=logger)
        apply_dry_run_arg(args)

        *names, folder = args.paths
        folder = Path(folder)
        if args.is_all and names:
            skill_parser.error("--all takes only FOLDER, not skill names")
        if not args.is_all and not names:
            skill_parser.error("give 1+ skill names, or --all, before FOLDER")

        logger.enter("{} skill".format(PACKAGE_NAME))
        check_corpus_setup_for_cli()

        if args.is_all:
            names = None
        try:
            select_exportables(names)
        except ValueError as err:
            logger.critical(str(err))
            raise SystemExit(1) from err

        render_profile = resolve_render_profile(
            args,
            surface_profiles=get_surface_profiles(),
            default_show_comment=False,
        )
        version = get_consumer_version()

        if args.zip:
            logger.debug("export skills as zip packages")
            export_skills_as_zips(
                folder,
                version=version,
                render_profile=render_profile,
                names=names,
            )
            done_msg = "export skills as zip packages"
        else:
            logger.debug("export skills as folders")
            export_skills_as_folders(
                folder,
                version=version,
                render_profile=render_profile,
                names=names,
            )
            done_msg = "export skills as folders"

        logger.done(done_msg + "\t" + str(folder))

    skill_parser.set_defaults(func=_skill_main)
