"""
export.py

define ``export_codex_marketplace``
"""

from kaye_engine.cli.claude.plugin_marketplace_name import (
    get_marketplace_name,
)
from kaye_engine.cli.codex.platform import CODEX_PLATFORM
from kaye_engine.cli.plugin_platform import export as platform_export


def export_codex_marketplace(root, *, render_profile=None):
    """
    export every consumer's Codex plugin into ``<root>/plugins/`` and write
    ``<root>/.agents/plugins/marketplace.json`` listing them, named after
    the repo; with ``root`` the home folder this is the personal
    marketplace


    :param root: the marketplace root
    :type root: Path-like
    :param render_profile: forwarded to every skill render
    :type render_profile: RenderProfile, optional
    :return: path to the written marketplace.json
    :rtype: Path
    """
    return platform_export.export_marketplace(
        CODEX_PLATFORM,
        root,
        get_marketplace_name(),
        render_profile=render_profile,
    )
