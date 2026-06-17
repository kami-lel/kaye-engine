"""
export_plugin_as_folder.py

define ``export_plugin_as_folder``
"""

from importlib.metadata import metadata, version

from kaye import logger

from kaye import PROGRAM_NAME
from kaye.cli.cli_claude.claude_skill.export_skills_as_folders import (
    export_skills_as_folders,
)
from .manifest_plugin_json import ManifestPluginJson

# constants  ===================================================================

_SKILLS_DIR = "skills"


# entry point  #################################################################


def export_plugin_as_folder(parent_folder):
    """
    export all Kaye blueprints as a single Anthropic Claude plugin folder

    writes a ``<parent_folder>/<PROGRAM_NAME>/`` plugin directory containing
    a ``.claude-plugin/plugin.json`` manifest and a ``skills/`` directory
    with one skill folder per blueprint, prompt, and abbreviation group


    :param parent_folder: destination directory to write the plugin into
    :type parent_folder: Path-like
    :return: path to the created plugin directory
    :rtype: Path
    """
    plugin_root = parent_folder / PROGRAM_NAME

    logger.debug("writing plugin manifest")
    meta = metadata(PROGRAM_NAME)
    with ManifestPluginJson(plugin_root) as manifest:
        manifest.name = PROGRAM_NAME
        manifest.display_name = meta["Name"]
        manifest.version = version(PROGRAM_NAME)
        manifest.description = meta["Summary"]
        manifest.author_name = meta["Author"]
        manifest.author_email = meta.get("Author-Email", "")
        manifest.homepage = meta.get("Home-Page", "")
        manifest.repository = meta.get("Project-URL", "").split(", ")[-1] if meta.get("Project-URL") else ""
        manifest.keywords = ["prompt-engineering", "persona", "agent", PROGRAM_NAME]

    logger.debug("exporting blueprints as plugin skills")
    export_skills_as_folders(plugin_root / _SKILLS_DIR)

    logger.succ("export plugin:\t" + str(plugin_root))

    return plugin_root
