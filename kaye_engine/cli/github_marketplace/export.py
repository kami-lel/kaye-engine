"""
export.py

define ``get_github_marketplace_name``, ``export_github_marketplace`` --
one repo root both Claude and Codex add by URL
"""

from kaye_engine.cli.claude.platform import CLAUDE_PLATFORM
from kaye_engine.cli.codex.platform import CODEX_PLATFORM
from kaye_engine.cli.plugin_platform import export as platform_export
from kaye_engine.repo import get_repo_name

__all__ = (
    "MARKETPLACE_PLATFORMS",
    "OWNED_PATHS",
    "export_github_marketplace",
    "get_github_marketplace_name",
)

# constants  ###################################################################

# every platform the repo serves, with its plugins folder under the root
MARKETPLACE_PLATFORMS = (
    (CLAUDE_PLATFORM, "plugins/claude"),
    (CODEX_PLATFORM, "plugins/codex"),
)

# the only root entries the command writes; any other root file, eg
# README.md, belongs to the repo's owner
OWNED_PATHS = (".claude-plugin", ".agents", "plugins")

_NAME_SUFFIX = "-marketplace"


# Public API  ##################################################################


def get_github_marketplace_name():
    """
    :raises SystemExit: exit code 1, when the repo name is unset
    :return: the marketplace name, ``REPO-marketplace``, distinct from the
            local ``REPO`` marketplace so both can be added
    :rtype: str
    """
    return get_repo_name() + _NAME_SUFFIX


def export_github_marketplace(output, owner_distribution, render_profiles):
    """
    write a marketplace repo root into ``output``: per platform, every
    plugin consumer's plugin under ``plugins/<platform>/`` and the
    platform's marketplace manifest at the root; nothing outside
    ``OWNED_PATHS`` is written


    :param output: the repo root to write
    :type output: Path-like
    :param owner_distribution: installed distribution describing and
            owning the marketplace, the default consumer's
    :type owner_distribution: str
    :param render_profiles: render profile per platform name
    :type render_profiles: dict[str, RenderProfile]
    :return: path of each written marketplace manifest, Claude first
    :rtype: list[Path]
    """
    name = get_github_marketplace_name()
    return [
        platform_export.export_marketplace(
            platform,
            output,
            name,
            plugins_dir=plugins_dir,
            render_profile=render_profiles[platform.name],
            owner_distribution=owner_distribution,
        )
        for platform, plugins_dir in MARKETPLACE_PLATFORMS
    ]
