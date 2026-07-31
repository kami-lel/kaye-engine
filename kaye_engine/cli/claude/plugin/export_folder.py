"""
export_plugin_as_folder.py

define ``export_plugin_as_folder``
"""

from email.utils import parseaddr
from importlib.metadata import metadata, version

from kaye_engine import logger

from kaye_engine import PROGRAM_NAME, DISPLAY_NAME
from kaye_engine.cli.claude.skill.export_folders import (
    export_skills_as_folders,
)
from .manifest import ManifestPluginJson

# Bug exported folder structure contains name: kaye-engine

# constants  ===================================================================

_SKILLS_DIR = "skills"
_PLUGIN_KEYWORDS = ["prompt-engineering", "persona", "agent", PROGRAM_NAME]

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

    # FIXME utilize kamilog here
    # Fixme reads distribution metadata mid-export, so an uninstalled
    # source checkout raises PackageNotFoundError instead of failing early
    meta = metadata(PROGRAM_NAME)
    pkg_version = version(PROGRAM_NAME)
    pkg_author, pkg_author_email = parseaddr(meta.get("Author-email") or "")
    pkg_urls = dict(
        _url.split(", ", 1) for _url in meta.get_all("Project-URL") or []
    )
    pkg_homepage = pkg_urls.get("homepage", "")
    pkg_repository = pkg_urls.get("Repository", "")

    with ManifestPluginJson(plugin_root) as manifest:
        manifest.name = PROGRAM_NAME
        manifest.display_name = DISPLAY_NAME
        manifest.version = pkg_version
        manifest.description = meta["Summary"]
        manifest.author_name = pkg_author
        manifest.author_email = pkg_author_email
        manifest.homepage = pkg_homepage
        manifest.repository = pkg_repository
        manifest.keywords = _PLUGIN_KEYWORDS
        logger.succ("write plugin manifest:\t" + str(manifest.path))

    logger.debug("exporting blueprints as plugin skills")
    export_skills_as_folders(plugin_root / _SKILLS_DIR)

    logger.succ("export plugin:\t" + str(plugin_root))

    return plugin_root
