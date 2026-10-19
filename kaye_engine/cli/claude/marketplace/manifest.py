"""
manifest.py

define ``MarketplaceJson``
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

import kamilog
from kaye_engine.deed import track
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.dry_run import is_dry_run

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)


@dataclass
class MarketplacePlugin:
    """
    one plugin entry of a marketplace; optional fields are omitted from
    the file when empty
    """

    name: str
    source: str
    display_name: str = ""
    description: str = ""
    version: str = ""
    author_name: str = ""
    author_email: str = ""
    homepage: str = ""
    repository: str = ""
    license: str = ""
    keywords: list = field(default_factory=list)
    category: str = ""
    tags: list = field(default_factory=list)

    def as_dict(self):
        """
        :return: the JSON object of this entry
        :rtype: dict
        """
        entry = {"name": self.name, "source": self.source}
        if self.display_name:
            entry["displayName"] = self.display_name
        if self.description:
            entry["description"] = self.description
        if self.version:
            entry["version"] = self.version
        if self.author_name:
            author = {"name": self.author_name}
            if self.author_email:
                author["email"] = self.author_email
            entry["author"] = author
        for key, val in (
            ("homepage", self.homepage),
            ("repository", self.repository),
            ("license", self.license),
            ("keywords", self.keywords),
            ("category", self.category),
            ("tags", self.tags),
        ):
            if val:
                entry[key] = val
        return entry


class MarketplaceJson:  #########################################################
    """
    manage metadata and content writing for a Claude plugin marketplace file

    writes a ``.claude-plugin/marketplace.json`` at the marketplace root,
    listing one entry per added plugin; optional fields are omitted when empty


    :param folder_path: marketplace root directory to write
            ``.claude-plugin/marketplace.json`` into
    :type folder_path: Path-like
    :example:
    >>> with MarketplaceJson(marketplace_root) as market:
    ...     market.name = "kaye"
    ...     market.description = "Prompt engineering toolkit"
    ...     market.version = "1.0.0"
    ...     market.plugins.append(MarketplacePlugin("kaye", "./plugins/kaye"))
    """

    # constants  ===============================================================

    _MANIFEST_DIR = ".claude-plugin"
    _MANIFEST_FILE = "marketplace.json"
    _SCHEMA = "https://json.schemastore.org/claude-code-marketplace.json"

    # constructor  =============================================================

    def __init__(self, folder_path):
        self._folder_path = Path(folder_path)
        self._manifest_dir = self._folder_path / self._MANIFEST_DIR
        self.path = self._manifest_dir / self._MANIFEST_FILE

        # marketplace-level fields  --------------------------------------------

        self.name = ""
        self.description = ""
        self.version = ""
        self.owner_name = ""
        self.owner_email = ""

        self.plugins = []

    # support context manager  =================================================

    def __enter__(self):
        return self

    def __exit__(self, *args):
        owner = {"name": self.owner_name}
        if self.owner_email:
            owner["email"] = self.owner_email

        marketplace_data = {"$schema": self._SCHEMA, "name": self.name}
        if self.description:
            marketplace_data["description"] = self.description
        if self.version:
            marketplace_data["version"] = self.version
        marketplace_data["owner"] = owner
        marketplace_data["plugins"] = [p.as_dict() for p in self.plugins]

        if not self._manifest_dir.is_dir():
            with track(logger).create_dir(self._manifest_dir):
                if not is_dry_run():
                    self._manifest_dir.mkdir(parents=True, exist_ok=True)
        with track(logger).save_config(self.path):
            if not is_dry_run():
                self.path.write_text(
                    json.dumps(marketplace_data, indent=2) + "\n",
                    encoding="utf-8",
                )
