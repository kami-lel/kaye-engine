"""
export.py

define ``export_hermes_folder``
"""

from pathlib import Path

import kamilog
from kaye_engine.cli.dry_run import is_dry_run
from kaye_engine.cli.hermes import LOGGER_HERMES_NAME
from kaye_engine.cli.hermes.setup import (
    get_hermes_profile_blueprint_names,
    get_hermes_soul_blueprint_name,
)
from kaye_engine.consumer import get_consumer_canonical_name
from kaye_engine.prompt.blueprint import blueprint_registry
from kaye_engine.skill.export_folders import export_skills_as_folders

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_HERMES_NAME)

# constants  ###################################################################

SOUL_FILENAME = "SOUL.md"
SKILLS_SUBFOLDER = "skills"
PROFILES_SUBFOLDER = "profiles"

_FILE_ENCODING = "utf-8"

# helpers  #####################################################################


def _write_soul(path, blueprint_name, render_profile):
    """
    render the registered blueprint ``blueprint_name`` into ``path``,
    creating its folder first; every write is a deed, and a dry run
    touches nothing
    """
    path = Path(path)
    try:
        if not path.parent.is_dir():
            with logger.track.create_dir(path.parent):
                if not is_dry_run():
                    path.parent.mkdir(parents=True, exist_ok=True)

        content = blueprint_registry[blueprint_name].content(
            profile=render_profile
        )
        deed = (
            logger.track.owr_file if path.exists() else logger.track.create_file
        )
        with deed(path):
            if not is_dry_run():
                path.write_text(content, encoding=_FILE_ENCODING)
    except OSError as err:
        logger.critical("cannot write:\t" + str(path))
        raise SystemExit(1) from err


# entry point  #################################################################


def export_hermes_folder(folder, *, version, render_profile=None):
    """
    export the vault into a Hermes home directory

    writes the root ``SOUL.md``, one ``profiles/<name>/SOUL.md`` per
    configured profile, and every exportable as a skill folder under
    ``skills/<category>/``; configured by ``setup_hermes_cli(...)``


    :param folder: Hermes home directory
    :type folder: Path-like
    :param version: installed package version, stamped into every skill
    :type version: str
    :param render_profile: render options forwarded to every render
    :type render_profile: RenderProfile, optional
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_hermes_cli(...)`` or a file cannot be written
    """
    category = get_consumer_canonical_name()
    soul_name = get_hermes_soul_blueprint_name()
    profile_names = get_hermes_profile_blueprint_names()

    logger.enter("exporting a Hermes home directory")
    folder = Path(folder)

    _write_soul(folder / SOUL_FILENAME, soul_name, render_profile)
    for profile, blueprint_name in profile_names.items():
        _write_soul(
            folder / PROFILES_SUBFOLDER / profile / SOUL_FILENAME,
            blueprint_name,
            render_profile,
        )
    export_skills_as_folders(
        folder / SKILLS_SUBFOLDER / category,
        version=version,
        render_profile=render_profile,
    )
