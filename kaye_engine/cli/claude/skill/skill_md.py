"""
skill_md.py

define ``Skill``
"""

from pathlib import Path

from kaye_engine.cli.frontmatter_doc import FrontmatterDoc, dump_yaml
from kaye_engine.cli.exportable_abbr import ExportableAbbr
from kaye_engine.prompt.blueprint import BlueprintRegistry


class Skill(FrontmatterDoc):
    """
    a Claude agent skill document, written as ``SKILL.md`` inside the
    skill's own folder

    only frontmatter fields that differ from their default are emitted, so
    a minimal skill carries a minimal header


    :param name: skill name, also used as the skill folder basename
    :type name: str
    :param description: skill description
    :type description: str
    :param when_to_use: guidance on when the skill applies
    :type when_to_use: str
    :param license: license identifier; omitted when empty
    :type license: str
    :param compatibility: compatibility note; omitted when empty
    :type compatibility: str
    :param metadata: extra metadata fields; a ``version`` entry is always
            injected on render
    :type metadata: dict
    :param allowed_tools: tools the skill may use; omitted when empty
    :type allowed_tools: list[str]
    :param user_invocable: whether users may invoke the skill directly;
            default=True
    :type user_invocable: bool, optional
    :param paths: file globs the skill applies to; omitted when empty
    :type paths: list[str]
    :param body: markdown body written after the frontmatter block
    :type body: str
    :param version: installed package version
    :type version: str, optional
    :example:
    >>> # any Exportable, blueprint or abbr group alike
    ... Skill.from_exportable(exportable).write(parent_folder)
    """

    # Public Methods  ----------------------------------------------------------

    def write(self, parent_folder):
        """
        create the skill folder under ``parent_folder`` and write
        ``SKILL.md`` into it


        :param parent_folder: directory the skill folder is created under
        :type parent_folder: Path-like
        :return: the skill folder that was written
        :rtype: Path
        """
        folder = Path(parent_folder) / self.name
        folder.mkdir(parents=True, exist_ok=True)
        super().write(folder / self._FILENAME)

        return folder

    # implement FrontmatterDoc  ------------------------------------------------

    def _render_frontmatter(self):
        metadata = dict(self.metadata)
        metadata["version"] = self.version

        fields = {
            "name": self.name,
            "description": self.description,
            "when_to_use": self.when_to_use,
            "license": self.license,
            "compatibility": self.compatibility,
            "metadata": metadata,
            "allowed-tools": self.allowed_tools,
            "user-invocable": self.user_invocable,
            "paths": self.paths,
        }
        sparse = {
            key: value
            for key, value in fields.items()
            if value != self._DEFAULT_FRONTMATTER.get(key)
        }
        return dump_yaml(sparse)

    # fields  ------------------------------------------------------------------

    _FILENAME = "SKILL.md"

    _DEFAULT_FRONTMATTER = {
        "name": "",
        "description": "",
        "when_to_use": "",
        "license": "",
        "compatibility": "",
        "metadata": {},
        "allowed-tools": [],
        "user-invocable": True,
        "paths": [],
    }

    def __init__(
        self,
        name="",
        description="",
        when_to_use="",
        license="",
        compatibility="",
        metadata=None,
        allowed_tools=None,
        user_invocable=True,
        paths=None,
        body="",
        version="",
    ):
        self.name = name
        self.description = description
        self.when_to_use = when_to_use
        self.license = license
        self.compatibility = compatibility
        self.metadata = dict(metadata) if metadata else {}
        self.allowed_tools = list(allowed_tools) if allowed_tools else []
        self.user_invocable = user_invocable
        self.paths = list(paths) if paths else []
        self.body = body
        self.version = version

    # factory  -----------------------------------------------------------------

    @classmethod
    def from_exportable(cls, exportable, version="", render_kwargs=None):
        """
        dispatches on the concrete `Exportable` implementer -- this
        isinstance check lives here, in the Claude-specific translation
        layer, precisely because `Exportable` itself stays Claude-agnostic


        :param exportable: entry to render, either a `BlueprintRegistry`
                or an `ExportableAbbr` group
        :type exportable: Exportable
        :param version: installed package version, forwarded to
                :meth:`__init__`
        :type version: str, optional
        :param render_kwargs: render options forwarded to
                ``exportable.blueprint.generate_prompt(...)`` -- already
                resolved (e.g. via :func:`resolve_render_options`), so
                its ``affordances``/``conditional_sidecars`` already
                carry whatever surface derivation the caller wants
        :type render_kwargs: dict, optional
        :return: a skill built from ``exportable``'s content
        :rtype: Skill
        """
        if isinstance(exportable, BlueprintRegistry):
            sidecars = exportable.blueprint.sidecars
            return cls(
                name=exportable.canonical_name,
                description=sidecars.description,
                when_to_use=sidecars.when_to_use,
                paths=list(sidecars.globs) if sidecars.globs else [],
                user_invocable=exportable.user_invokable,
                body=exportable.blueprint.generate_prompt(
                    **(render_kwargs or {})
                ),
                version=version,
            )

        assert isinstance(exportable, ExportableAbbr)
        return cls(
            name=exportable.canonical_name,
            description=exportable.display_name,
            user_invocable=exportable.user_invokable,
            body=exportable.as_md_list(),
            version=version,
        )
