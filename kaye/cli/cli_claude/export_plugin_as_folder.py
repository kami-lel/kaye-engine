"""
export_plugin_as_folder.py

define ``export_plugin_as_folder``
"""

import json
from importlib.metadata import metadata, version

from kaye import logger

from kaye import PROGRAM_NAME
from kaye.cli.cli_claude.export_skills_as_folders import (
    export_skills_as_folders,
)

# constants  ===================================================================

_MANIFEST_DIR = ".claude-plugin"
_MANIFEST_FILE = "plugin.json"
_SKILLS_DIR = "skills"


# entry point  #################################################################


def export_plugin_as_folder(parent_folder, *, verbose=True):
    """
    export all Kaye blueprints as a single Anthropic Claude plugin folder

    writes a ``<parent_folder>/<PROGRAM_NAME>/`` plugin directory containing
    a ``.claude-plugin/plugin.json`` manifest and a ``skills/`` directory
    with one skill folder per blueprint, prompt, and abbreviation group


    :param parent_folder: destination directory to write the plugin into
    :type parent_folder: Path-like
    :param verbose: print exported skill and plugin paths when ``True``
    :type verbose: bool
    :returns: path to the created plugin directory
    :rtype: Path
    """
    plugin_root = parent_folder / PROGRAM_NAME

    logger.debug("creating plugin manifest directory")
    manifest_dir = plugin_root / _MANIFEST_DIR
    manifest_dir.mkdir(parents=True, exist_ok=True)

    logger.debug("writing plugin manifest")
    manifest_path = manifest_dir / _MANIFEST_FILE
    manifest_path.write_text(
        json.dumps(_build_manifest(), indent=2) + "\n",
        encoding="utf-8",
    )

    logger.debug("exporting blueprints as plugin skills")
    export_skills_as_folders(plugin_root / _SKILLS_DIR, verbose=verbose)

    logger.succ("export plugin:\t" + str(plugin_root))

    return plugin_root


def _build_manifest():
    """
    build the ``plugin.json`` manifest dict from packaged metadata

    :returns: manifest mapping ready for JSON serialization
    :rtype: dict
    """
    meta = metadata(PROGRAM_NAME)

    return {
        "name": PROGRAM_NAME,
        "displayName": meta["Name"],
        "version": version(PROGRAM_NAME),
        "description": meta["Summary"],
        "author": {"name": meta["Author"]},
        "keywords": ["prompt-engineering", "persona", "agent", PROGRAM_NAME],
    }
