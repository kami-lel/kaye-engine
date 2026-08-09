"""
registry.py

define `BlueprintRegistry`, `register_blueprint`, `blueprint_registry`
"""

from dataclasses import dataclass

from kaye_engine.exportable import Exportable, register_exportable_entry

from .prompt_blueprint import PromptBlueprint

__all__ = (
    "BlueprintRegistry",
    "register_blueprint",
    "get_blueprint",
    "blueprint_registry",
)


@dataclass(kw_only=True)
class BlueprintRegistry(Exportable):
    """
    metadata & export policy for a single named `PromptBlueprint`

    instances are created via `register_blueprint` and collected in
    `blueprint_registry`, keyed by their `canonical_name`; this is the
    single source of truth for a blueprint's identity and where it
    should be exported (Claude skills) and how -- it implements
    `Exportable` directly, so a registered, exportable instance is also
    the entry stored in `exportable_registry` under the same key


    :param blueprint: the underlying blueprint
    :type blueprint: PromptBlueprint
    :param is_internal: never export this blueprint as a Claude Agent
            Skill; defaults to False
    :type is_internal: bool, optional
    """

    blueprint: PromptBlueprint
    is_internal: bool = False

    def content(self):
        """
        :return: this blueprint's rendered prompt
        :rtype: str
        """
        return self.blueprint.generate_prompt(sparseness=0)


# Entry Point  #################################################################

blueprint_registry = {}


def register_blueprint(
    canonical_name,
    display_name,
    blueprint,
    *,
    is_internal=False,
    always_apply=False,
    user_invokable=True,
    llm_invokable=True,
):
    """
    create a `BlueprintRegistry` and insert it into `blueprint_registry`;
    unless ``is_internal``, the same instance is also inserted into
    `exportable_registry` via `register_exportable_entry`


    :param canonical_name: kebab-case name, used directly as the
            exported skill name when not ``is_internal``
    :type canonical_name: str
    :param display_name: human-readable name, e.g. ``"Coder Python"``
    :type display_name: str
    :param blueprint: the underlying blueprint
    :type blueprint: PromptBlueprint
    :param is_internal: never export this blueprint as a Claude Agent
            Skill; defaults to False
    :type is_internal: bool, optional
    :param always_apply: whether this entry is unconditionally relevant
            and should always be applied, rather than surfaced only when
            judged relevant; defaults to False
    :type always_apply: bool, optional
    :param user_invokable: whether a human may deliberately invoke this
            entry by name, rather than it only ever surfacing on its
            own; defaults to True
    :type user_invokable: bool, optional
    :param llm_invokable: whether the assistant may bring this entry
            into play on its own judgment, without being explicitly
            named; defaults to True
    :type llm_invokable: bool, optional
    :raise ValueError: ``canonical_name`` is already registered
    :return: the created registry entry
    :rtype: BlueprintRegistry
    """
    if canonical_name in blueprint_registry:
        raise ValueError(
            "duplicate blueprint registry name: {}".format(canonical_name)
        )

    reg = BlueprintRegistry(
        canonical_name=canonical_name,
        display_name=display_name,
        blueprint=blueprint,
        is_internal=is_internal,
        always_apply=always_apply,
        user_invokable=user_invokable,
        llm_invokable=llm_invokable,
    )
    blueprint_registry[canonical_name] = reg

    if not is_internal:
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
    """
    try:
        return blueprint_registry[canonical_name]
    except KeyError as e:
        raise KeyError(
            "no blueprint registered under name: {}".format(canonical_name)
        ) from e
