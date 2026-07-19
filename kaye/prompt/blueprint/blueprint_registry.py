"""
blueprint_registry.py

define `BlueprintRegistry`, `register_blueprint`, `BLUEPRINT_REGISTRIES`
"""

from dataclasses import dataclass

from .prompt_blueprint import PromptBlueprint

__all__ = ("BlueprintRegistry", "register_blueprint", "BLUEPRINT_REGISTRIES")


@dataclass
class BlueprintRegistry:
    """
    metadata & export policy for a single named `PromptBlueprint`

    instances are created via `register_blueprint` and collected in
    `BLUEPRINT_REGISTRIES`; this is the single source of truth for a
    blueprint's identity (`name`/`display_name`) and where it should be
    exported (Continue AI rules, Claude skills) and how


    :param name: canonical string key, kebab-case, e.g. ``"coder-py"``,
            ``"rapid"``
    :type name: str
    :param display_name: human-readable name, e.g. ``"Coder Python"``
    :type display_name: str
    :param blueprint: the underlying blueprint
    :type blueprint: PromptBlueprint
    :param skill_exportable: export as a Claude Agent Skill;
            defaults to False
    :type skill_exportable: bool, optional
    :param continue_exportable: export as a Continue AI rule;
            defaults to False
    :type continue_exportable: bool, optional
    :param always_apply: mark the exported Continue AI rule as
            ``alwaysApply``; defaults to False
    :type always_apply: bool, optional
    :param invokable: mark the exported Continue AI rule as
            ``invokable``; defaults to False
    :type invokable: bool, optional
    """

    name: str
    display_name: str
    blueprint: PromptBlueprint
    skill_exportable: bool = False
    continue_exportable: bool = False
    always_apply: bool = False
    invokable: bool = False


# Entry Point  #################################################################

BLUEPRINT_REGISTRIES = {}


def register_blueprint(
    name,
    display_name,
    blueprint,
    *,
    skill_exportable=False,
    continue_exportable=False,
    always_apply=False,
    invokable=False,
):
    """
    create a `BlueprintRegistry` and insert it into `BLUEPRINT_REGISTRIES`


    :param name: canonical string key, kebab-case, must be unique across
            all registrations
    :type name: str
    :param display_name: human-readable name
    :type display_name: str
    :param blueprint: the underlying blueprint
    :type blueprint: PromptBlueprint
    :param skill_exportable: defaults to False
    :type skill_exportable: bool, optional
    :param continue_exportable: defaults to False
    :type continue_exportable: bool, optional
    :param always_apply: defaults to False
    :type always_apply: bool, optional
    :param invokable: defaults to False
    :type invokable: bool, optional
    :raise ValueError: ``name`` is already registered
    :return: the created registry entry
    :rtype: BlueprintRegistry
    """
    if name in BLUEPRINT_REGISTRIES:
        raise ValueError(
            "duplicate blueprint registry name: {}".format(name)
        )

    reg = BlueprintRegistry(
        name=name,
        display_name=display_name,
        blueprint=blueprint,
        skill_exportable=skill_exportable,
        continue_exportable=continue_exportable,
        always_apply=always_apply,
        invokable=invokable,
    )
    BLUEPRINT_REGISTRIES[name] = reg

    return reg
