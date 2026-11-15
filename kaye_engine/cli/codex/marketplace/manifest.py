"""
manifest.py

define ``CodexMarketplacePlugin``, ``CodexMarketplace``
"""

from dataclasses import dataclass, field
from pathlib import Path

from kaye_engine.cli.plugin_platform.json_file import write_json_file

__all__ = ("CodexMarketplace", "CodexMarketplacePlugin")


@dataclass
class CodexMarketplacePlugin:
    """
    one plugin entry of a Codex marketplace, a local plugin folder
    """

    name: str
    path: str
    category: str = "Productivity"
    installation: str = "AVAILABLE"
    authentication: str = "ON_INSTALL"

    def as_dict(self):
        """
        :return: the JSON object of this entry
        :rtype: dict
        """
        return {
            "name": self.name,
            "source": {"source": "local", "path": self.path},
            "policy": {
                "installation": self.installation,
                "authentication": self.authentication,
            },
            "category": self.category,
        }


@dataclass
class CodexMarketplace:
    """
    a Codex marketplace catalog, written as
    ``<root>/.agents/plugins/marketplace.json``; every plugin ``path`` is
    relative to ``root``
    """

    name: str
    display_name: str = ""
    plugins: list = field(default_factory=list)

    # constants  ===============================================================

    MANIFEST_PATH = (".agents", "plugins", "marketplace.json")

    # Public API  ==============================================================

    def as_dict(self):
        """
        :return: the JSON object of the catalog
        :rtype: dict
        """
        data = {"name": self.name}
        if self.display_name:
            data["interface"] = {"displayName": self.display_name}
        data["plugins"] = [p.as_dict() for p in self.plugins]
        return data

    def write(self, logger, root):
        """
        :param logger: logger every deed reports through
        :type logger: kamilog.Logger
        :param root: the marketplace root
        :type root: Path-like
        :return: path to the written catalog
        :rtype: Path
        """
        path = Path(root).joinpath(*self.MANIFEST_PATH)
        write_json_file(logger, path, self.as_dict())
        return path.resolve()
