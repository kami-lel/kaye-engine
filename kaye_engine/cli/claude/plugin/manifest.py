"""
manifest.py

define ``ManifestPluginJson``
"""

import json
from pathlib import Path


class ManifestPluginJson:  #######################################################
    """
    manage metadata and content writing for a Claude plugin manifest file


    :param folder_path: folder to write plugin.json into
    :type folder_path: Path-like
    :example:
    >>> with ManifestPluginJson(plugin_folder) as manifest:
    ...     manifest.name = "kaye"
    ...     manifest.version = "1.0.0"
    ...     manifest.description = "Prompt engineering toolkit"
    ...     ~~
    """

    # constants  ===============================================================

    _MANIFEST_DIR = ".claude-plugin"
    _MANIFEST_FILE = "plugin.json"

    # constructor  =============================================================

    def __init__(self, folder_path):
        self._folder_path = Path(folder_path)
        self._manifest_dir = self._folder_path / self._MANIFEST_DIR
        self.path = self._manifest_dir / self._MANIFEST_FILE

        self.name = ""
        self.display_name = ""
        self.version = ""
        self.description = ""
        self.author_name = ""
        self.author_email = ""
        self.author_url = ""
        self.homepage = ""
        self.repository = ""
        self.keywords = []

    # support context manager  =================================================

    def __enter__(self):
        return self

    def __exit__(self, *args):
        manifest_data = {
            "name": self.name,
            "displayName": self.display_name,
            "version": self.version,
            "description": self.description,
            "author": {
                "name": self.author_name,
                "email": self.author_email,
                "url": self.author_url,
            },
            "homepage": self.homepage,
            "repository": self.repository,
            "keywords": self.keywords,
        }

        # Fixme utilize kamilog here
        self._manifest_dir.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(manifest_data, indent=2) + "\n",
            encoding="utf-8",
        )
