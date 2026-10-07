"""
registry.py

define `BlueprintRegistry`, `register_blueprint`, `blueprint_registry`
"""

from dataclasses import dataclass, replace

from kaye_engine.exportable import Exportable, register_exportable_entry

from .data import Blueprint
from .render.prompt import render_prompt
from .render_profile import RenderProfile
from .validate import validate_blueprint

__all__ = (
    "BlueprintRegistry",
    "blueprint_registry",
    "get_blueprint",
    "register_blueprint",
)


@dataclass(kw_only=True)
class BlueprintRegistry(Exportable):
    """
    metadata & export policy for a single named `Blueprint`

    instances are created via `register_blueprint` and collected in
    `blueprint_registry`, keyed by their `canonical_name`; this is the
    single source of truth for a blueprint's identity and where it
    should be exported (Agent Skills) and how -- it implements
    `Exportable` directly, so a registered, exportable instance is also
    the entry stored in `exportable_registry` under the same key


    :param blueprint: the underlying blueprint
    :type blueprint: Blueprint
    :param display_name: fallback name, used only when the blueprint's
            meta has none; reading ``display_name`` gives the meta name
            first; defaults to ``""``
    :type display_name: str, optional
    :param is_exportable: whether this blueprint is exported as a Claude
            Agent Skill; defaults to True
    :type is_exportable: bool, optional
    """

    blueprint: Blueprint
    is_exportable: bool = True

    supports_negative_content = True

    @property
    def display_name(self):
        """
        read live, so a reassigned ``blueprint`` with a new meta name
        shows at once


        :return: the blueprint's meta display name, else the fallback,
                else ``""``
        :rtype: str
        """
        return self.blueprint.meta.display_name or self._fallback_name

    @display_name.setter
    def display_name(self, value):
        self._fallback_name = value

    def resolve_profile(self, profile=None):
        """
        :param profile: render profile merged with this registry
                entry's own `render_profile`, not replaced by it
        :type profile: RenderProfile, optional
        :return: the profile to render this entry with; its comment is
                named after this entry unless the caller chose a name
        :rtype: RenderProfile
        """
        merged = self.render_profile
        if profile is not None:
            merged = merged.merge(profile)
        if not merged.display_name:
            merged = replace(merged, display_name=self.display_name)
        return merged

    def content(self, *, profile=None, **kwargs):
        """
        :param profile: see :meth:`resolve_profile`
        :type profile: RenderProfile, optional
        :param kwargs: further render options (e.g. ``query``)
                forwarded to ``render_prompt(...)``
        :return: this blueprint's rendered prompt
        :rtype: str
        """
        return render_prompt(
            self.blueprint, profile=self.resolve_profile(profile), **kwargs
        )


# Entry Point  #################################################################

blueprint_registry = {}


def register_blueprint(
    canonical_name,
    blueprint,
    *,
    display_name="",
    is_exportable=True,
    is_user_invokable=True,
    llm_invokable=True,
    always_apply=False,
    render_profile=RenderProfile(),
):
    """
    create a `BlueprintRegistry` and insert it into `blueprint_registry`;
    when ``is_exportable``, the same instance is also inserted into
    `exportable_registry` via `register_exportable_entry`


    :param canonical_name: kebab-case name, used directly as the
            exported skill name when ``is_exportable``
    :type canonical_name: str
    :param blueprint: the underlying blueprint; its meta display name is
            the entry's display name
    :type blueprint: Blueprint
    :param display_name: fallback name, used only when the blueprint's
            meta has none; defaults to ``""``
    :type display_name: str, optional
    :param is_exportable: whether this blueprint is exported as a Claude
            Agent Skill; defaults to True
    :type is_exportable: bool, optional
    :param is_user_invokable: whether a human may deliberately invoke this
            entry by name, rather than it only ever surfacing on its
            own; defaults to True
    :type is_user_invokable: bool, optional
    :param llm_invokable: whether the assistant may bring this entry
            into play on its own judgment, without being explicitly
            named; defaults to True
    :type llm_invokable: bool, optional
    :param always_apply: whether the entry is unconditionally relevant
            and always applied, rather than surfaced only when judged
            relevant; defaults to False
    :type always_apply: bool, optional
    :param render_profile: default render settings for this entry,
            merged with any caller-supplied profile unless the caller
            passes its own value explicitly; defaults to a plain
            `RenderProfile()`
    :type render_profile: RenderProfile, optional
    :raises ValueError: ``canonical_name`` is already registered, a
            dependency name is not registered, or (while a corpus is
            loaded) a node path is not in it
    :return: the created registry entry
    :rtype: BlueprintRegistry
    :example:
    >>> register_blueprint("coder", coder_blueprint)
    >>> register_blueprint("chat", chat_blueprint, is_exportable=False)
    """
    if canonical_name in blueprint_registry:
        raise ValueError(
            "duplicate blueprint registry name: {}".format(canonical_name)
        )

    validate_blueprint(blueprint)

    reg = BlueprintRegistry(
        canonical_name=canonical_name,
        blueprint=blueprint,
        display_name=display_name,
        is_exportable=is_exportable,
        is_user_invokable=is_user_invokable,
        llm_invokable=llm_invokable,
        always_apply=always_apply,
        render_profile=render_profile,
    )
    blueprint_registry[canonical_name] = reg

    if is_exportable:
        register_exportable_entry(reg)

    return reg


def get_blueprint(canonical_name):
    """
    :param canonical_name: canonical string key a blueprint was
            registered under via `register_blueprint`
    :type canonical_name: str
    :raises KeyError: no blueprint is registered under ``canonical_name``
    :return: the registry entry stored under ``canonical_name``
    :rtype: BlueprintRegistry
    :example:
    >>> get_blueprint("coder")
    """
    try:
        return blueprint_registry[canonical_name]
    except KeyError as e:
        raise KeyError(
            "no blueprint registered under name: {}".format(canonical_name)
        ) from e
