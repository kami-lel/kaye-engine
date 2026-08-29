"""
base.py

define ``Exportable``
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from kaye_engine.prompt.blueprint.render_profile import RenderProfile

__all__ = ("Exportable",)


@dataclass(kw_only=True)
class Exportable(ABC):
    """
    common interface and shared metadata for anything that can appear in
    `exportable_registry`

    `BlueprintRegistry` and `ExportableAbbr` are its two concrete
    implementers -- there is no separate wrapper class in between; the
    registry entry or abbr group *is* the `Exportable` stored under its
    `canonical_name`


    :param canonical_name: kebab-case name, used directly as the
            exported skill name
    :type canonical_name: str
    :param display_name: human-readable name
    :type display_name: str
    :param is_user_invokable: whether a human may deliberately invoke this
            entry by name, rather than it only ever surfacing on its
            own; defaults to True
    :type is_user_invokable: bool, optional
    :param llm_invokable: whether the assistant may bring this entry
            into play on its own judgment, without being explicitly
            named; defaults to True
    :type llm_invokable: bool, optional
    :param render_profile: default render settings for this entry,
            merged with any caller-supplied profile rather than
            replaced by it; defaults to a plain `RenderProfile()`
    :type render_profile: RenderProfile, optional
    """

    canonical_name: str
    display_name: str
    is_user_invokable: bool = True
    llm_invokable: bool = True

    render_profile: RenderProfile = field(default_factory=RenderProfile)

    @abstractmethod
    def content(self, **kwargs):
        """
        generic, non-Claude-specific displayable content -- e.g. the
        rendered prompt for a blueprint, or the markdown abbr list for
        an abbr group; used by the ``kaye-engine exportable`` CLI
        command


        :param kwargs: render options forwarded to
                ``PromptBlueprint.generate_prompt(...)`` by
                implementers that render a blueprint; ignored by
                implementers that don't
        :return: this exportable's content
        :rtype: str
        """
