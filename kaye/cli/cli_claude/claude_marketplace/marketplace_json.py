"""
marketplace_json.py

define ``MarketplaceJson``
"""

import json
from pathlib import Path


class MarketplaceJson:  #########################################################
    """
    manage metadata and content writing for a Claude plugin marketplace file

    writes a ``.claude-plugin/marketplace.json`` at the marketplace root,
    listing a single plugin entry; optional fields are omitted when empty


    :param folder_path: marketplace root directory to write
            ``.claude-plugin/marketplace.json`` into
    :type folder_path: Path-like
    :example:
    >>> with MarketplaceJson(marketplace_root) as market:
    ...     market.name = "kaye"
    ...     market.description = "Prompt engineering toolkit"
    ...     market.version = "1.0.0"
    ...     ~~
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

        # plugin entry fields  -------------------------------------------------

        self.plugin_name = ""
        self.plugin_source = ""
        self.plugin_display_name = ""
        self.plugin_description = ""
        self.plugin_version = ""
        self.plugin_author_name = ""
        self.plugin_author_email = ""
        self.plugin_homepage = ""
        self.plugin_repository = ""
        self.plugin_license = ""
        self.plugin_keywords = []
        self.plugin_category = ""
        self.plugin_tags = []

    # support context manager  =================================================

    def __enter__(self):
        return self

    def __exit__(self, *args):
        owner = {"name": self.owner_name}
        if self.owner_email:
            owner["email"] = self.owner_email

        plugin_entry = {
            "name": self.plugin_name,
            "source": self.plugin_source,
        }
        if self.plugin_display_name:
            plugin_entry["displayName"] = self.plugin_display_name
        if self.plugin_description:
            plugin_entry["description"] = self.plugin_description
        if self.plugin_version:
            plugin_entry["version"] = self.plugin_version
        if self.plugin_author_name:
            author = {"name": self.plugin_author_name}
            if self.plugin_author_email:
                author["email"] = self.plugin_author_email
            plugin_entry["author"] = author
        if self.plugin_homepage:
            plugin_entry["homepage"] = self.plugin_homepage
        if self.plugin_repository:
            plugin_entry["repository"] = self.plugin_repository
        if self.plugin_license:
            plugin_entry["license"] = self.plugin_license
        if self.plugin_keywords:
            plugin_entry["keywords"] = self.plugin_keywords
        if self.plugin_category:
            plugin_entry["category"] = self.plugin_category
        if self.plugin_tags:
            plugin_entry["tags"] = self.plugin_tags

        marketplace_data = {"$schema": self._SCHEMA, "name": self.name}
        if self.description:
            marketplace_data["description"] = self.description
        if self.version:
            marketplace_data["version"] = self.version
        marketplace_data["owner"] = owner
        marketplace_data["plugins"] = [plugin_entry]

        self._manifest_dir.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(marketplace_data, indent=2) + "\n",
            encoding="utf-8",
        )
