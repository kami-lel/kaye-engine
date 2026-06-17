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
from .marketplace_json import MarketplaceJson

# constants  ===================================================================

_SKILLS_DIR = "skills"
_PLUGIN_KEYWORDS = ["prompt-engineering", "persona", "agent", PROGRAM_NAME]
_PLUGIN_CATEGORY = "productivity"

# entry point  #################################################################


def export_plugin_as_folder(parent_folder):
    """
    export all Kaye blueprints as a single Anthropic Claude plugin folder

    writes a ``<parent_folder>/<PROGRAM_NAME>/`` plugin directory containing
    a ``.claude-plugin/plugin.json`` manifest and a ``skills/`` directory
    with one skill folder per blueprint, prompt, and abbreviation group;
    also writes a ``.claude-plugin/marketplace.json`` at ``parent_folder``


    :param parent_folder: destination directory to write the plugin into
    :type parent_folder: Path-like
    :return: path to the created plugin directory
    :rtype: Path
    """
    plugin_root = parent_folder / PROGRAM_NAME

    meta = metadata(PROGRAM_NAME)
    pkg_version = version(PROGRAM_NAME)
    pkg_author = meta["Author"] or ""
    pkg_author_email = meta.get("Author-Email") or ""
    pkg_homepage = meta.get("Home-Page") or ""
    pkg_repository = (
        meta.get("Project-URL", "").split(", ")[-1]
        if meta.get("Project-URL")
        else ""
    )

    with ManifestPluginJson(plugin_root) as manifest:
        manifest.name = PROGRAM_NAME
        manifest.display_name = meta["Name"]
        manifest.version = pkg_version
        manifest.description = meta["Summary"]
        manifest.author_name = pkg_author
        manifest.author_email = pkg_author_email
        manifest.homepage = pkg_homepage
        manifest.repository = pkg_repository
        manifest.keywords = _PLUGIN_KEYWORDS
        logger.succ("write plugin manifest:\t" + str(manifest.path))

    with MarketplaceJson(parent_folder) as market:
        market.name = PROGRAM_NAME
        market.description = meta["Summary"]
        market.version = pkg_version
        market.owner_name = pkg_author
        market.owner_email = pkg_author_email
        market.plugin_name = PROGRAM_NAME
        market.plugin_source = "./" + PROGRAM_NAME
        market.plugin_display_name = meta["Name"]
        market.plugin_description = meta["Summary"]
        market.plugin_version = pkg_version
        market.plugin_author_name = pkg_author
        market.plugin_author_email = pkg_author_email
        market.plugin_homepage = pkg_homepage
        market.plugin_repository = pkg_repository
        market.plugin_keywords = _PLUGIN_KEYWORDS
        market.plugin_category = _PLUGIN_CATEGORY
        logger.succ("write marketplace manifest:\t" + str(market.path))

    logger.debug("exporting blueprints as plugin skills")
    export_skills_as_folders(plugin_root / _SKILLS_DIR)

    logger.succ("export plugin:\t" + str(plugin_root))

    return plugin_root
