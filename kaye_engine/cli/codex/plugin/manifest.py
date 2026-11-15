"""
manifest.py

define ``CodexPluginManifest``
"""

from dataclasses import dataclass, field
from pathlib import Path

from kaye_engine.cli.plugin_platform.json_file import write_json_file

__all__ = ("CodexPluginManifest",)


@dataclass
class CodexPluginManifest:
    """
    metadata of one Codex plugin, written as 2 manifests: the portable
    root ``plugin.json`` (Agent Plugins core fields) and the Codex
    ``.codex-plugin/plugin.json`` (core fields plus ``skills`` and the
    OpenAI ``interface``); empty fields are omitted from both

    the root manifest carries no ``extensions`` object, so Codex reads its
    OpenAI presentation from ``.codex-plugin/plugin.json``
    """

    name: str
    version: str = ""
    description: str = ""
    display_name: str = ""
    author_name: str = ""
    author_email: str = ""
    homepage: str = ""
    repository: str = ""
    keywords: list = field(default_factory=list)
    category: str = "Productivity"

    # constants  ===============================================================

    SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    ROOT_FILE = "plugin.json"
    CODEX_DIR = ".codex-plugin"
    SKILLS_PATH = "./skills/"

    # Public API  ==============================================================

    def core_dict(self):
        """
        :return: the fields both manifests share, empty ones omitted
        :rtype: dict
        """
        data = {"name": self.name}
        for key, val in (
            ("version", self.version),
            ("description", self.description),
        ):
            if val:
                data[key] = val
        if self.author_name:
            author = {"name": self.author_name}
            if self.author_email:
                author["email"] = self.author_email
            data["author"] = author
        for key, val in (
            ("homepage", self.homepage),
            ("repository", self.repository),
            ("keywords", self.keywords),
        ):
            if val:
                data[key] = val
        return data

    def root_dict(self):
        """
        :return: the portable root ``plugin.json``
        :rtype: dict
        """
        return {"$schema": self.SCHEMA, **self.core_dict()}

    def codex_dict(self):
        """
        :return: the Codex ``.codex-plugin/plugin.json``
        :rtype: dict
        """
        interface = {}
        for key, val in (
            ("displayName", self.display_name),
            ("shortDescription", self.description),
            ("developerName", self.author_name),
            ("category", self.category),
        ):
            if val:
                interface[key] = val

        data = self.core_dict()
        data["skills"] = self.SKILLS_PATH
        if interface:
            data["interface"] = interface
        return data

    def write(self, logger, plugin_root):
        """
        write both manifests into ``plugin_root``


        :param logger: logger every deed reports through
        :type logger: kamilog.Logger
        :param plugin_root: the plugin's own folder
        :type plugin_root: Path-like
        :return: path of the root manifest, then the Codex manifest
        :rtype: tuple[Path, Path]
        """
        plugin_root = Path(plugin_root)
        root_path = plugin_root / self.ROOT_FILE
        codex_path = plugin_root / self.CODEX_DIR / self.ROOT_FILE
        write_json_file(logger, root_path, self.root_dict())
        write_json_file(logger, codex_path, self.codex_dict())
        return root_path, codex_path
