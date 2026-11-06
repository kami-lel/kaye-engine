"""
export.py

define ``export_hermes_folder``
"""

from pathlib import Path

import kamilog
from kaye_engine.deed import track
from kaye_engine.cli.dry_run import is_dry_run
from kaye_engine.cli.file_write import write_text_if_changed
from kaye_engine.cli.hermes import LOGGER_HERMES_NAME
from kaye_engine.cli.hermes.setup import (
    get_hermes_profile_blueprint_names,
    get_hermes_soul_blueprint_name,
)
from kaye_engine.cli.claude.plugin_marketplace_name import (
    get_plugin_consumers,
)
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
            with track(logger).create_dir(path.parent):
                if not is_dry_run():
                    path.parent.mkdir(parents=True, exist_ok=True)

        content = blueprint_registry[blueprint_name].content(
            profile=render_profile
        )
        write_text_if_changed(
            logger, path, content, encoding=_FILE_ENCODING
        )
    except OSError as err:
        logger.critical("cannot write:\t" + str(path))
        raise SystemExit(1) from err


def _export_skills(home, render_profile):
    """
    export every consumer's exportables as skill folders under
    ``home/skills/<consumer>/``
    """
    for consumer in get_plugin_consumers():
        export_skills_as_folders(
            home / SKILLS_SUBFOLDER / consumer.canonical_name,
            version=consumer.version,
            render_profile=render_profile,
            consumer=consumer.canonical_name,
        )


# entry point  #################################################################


def export_hermes_folder(folder, *, render_profile=None):
    """
    export the registered prompts into a Hermes home directory

    writes the root ``SOUL.md``, one ``profiles/<name>/SOUL.md`` per
    configured profile, and every exportable as a skill folder under
    ``skills/<consumer>/``, one per consumer holding any, in the root and
    in each profile folder; configured by ``setup_hermes_cli(...)``


    :param folder: Hermes home directory
    :type folder: Path-like
    :param render_profile: render options forwarded to every render
    :type render_profile: RenderProfile, optional
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_hermes_cli(...)`` or a file cannot be written
    """
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
    # default profile (root) and every named profile each hold all skills
    homes = [folder]
    homes += [folder / PROFILES_SUBFOLDER / name for name in profile_names]
    for home in homes:
        _export_skills(home, render_profile)
