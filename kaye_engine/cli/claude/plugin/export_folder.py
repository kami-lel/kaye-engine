"""
export_plugin_as_folder.py

define ``export_plugin_as_folder``
"""

from email.utils import parseaddr
from importlib.metadata import PackageNotFoundError, metadata, version

from kaye_engine import DISPLAY_NAME, PACKAGE_NAME, kamilog
from kaye_engine.cli import claude
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.claude.skill.export_folders import (
    export_skills_as_folders,
)
from .manifest import ManifestPluginJson

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ===================================================================

_SKILLS_DIR = "skills"

# entry point  #################################################################


def export_plugin_as_folder(parent_folder):
    """
    export all Kaye blueprints as a single Anthropic Claude plugin folder

    writes a ``<parent_folder>/<PLUGIN_MARKETPLACE_NAME>/`` plugin directory
    containing a ``.claude-plugin/plugin.json`` manifest and a ``skills/``
    directory with one skill folder per blueprint, prompt, and abbreviation
    group


    :param parent_folder: destination directory to write the plugin into
    :type parent_folder: Path-like
    :return: path to the created plugin directory
    :rtype: Path
    """
    plugin_keywords = [
        "prompt-engineering",
        "persona",
        "agent",
        claude.PLUGIN_MARKETPLACE_NAME,
    ]
    plugin_root = parent_folder / claude.PLUGIN_MARKETPLACE_NAME

    # Fixme reads distribution metadata mid-export, so an uninstalled
    # source checkout raises PackageNotFoundError instead of failing early
    try:
        meta = metadata(PACKAGE_NAME)
        pkg_version = version(PACKAGE_NAME)
    except PackageNotFoundError as err:
        logger.critical("package metadata not found:\t" + PACKAGE_NAME)
        raise SystemExit(1) from err
    pkg_author, pkg_author_email = parseaddr(meta.get("Author-email") or "")
    pkg_urls = dict(
        _url.split(", ", 1) for _url in meta.get_all("Project-URL") or []
    )
    pkg_homepage = pkg_urls.get("homepage", "")
    pkg_repository = pkg_urls.get("Repository", "")

    with ManifestPluginJson(plugin_root) as manifest:
        manifest.name = claude.PLUGIN_MARKETPLACE_NAME
        manifest.display_name = DISPLAY_NAME
        manifest.version = pkg_version
        manifest.description = meta["Summary"]
        manifest.author_name = pkg_author
        manifest.author_email = pkg_author_email
        manifest.homepage = pkg_homepage
        manifest.repository = pkg_repository
        manifest.keywords = plugin_keywords
        logger.succ("write plugin manifest:\t" + str(manifest.path))

    logger.debug("exporting blueprints as plugin skills")
    export_skills_as_folders(plugin_root / _SKILLS_DIR)

    logger.succ("export plugin:\t" + str(plugin_root))

    return plugin_root
