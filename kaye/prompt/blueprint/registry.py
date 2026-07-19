"""
registry.py

define `BlueprintRegistry`, `register_blueprint`, `BLUEPRINT_REGISTRIES`
"""

import re

from dataclasses import dataclass

from .prompt_blueprint import PromptBlueprint

__all__ = (
    "BlueprintRegistry",
    "register_blueprint",
    "BLUEPRINT_REGISTRIES",
    "to_skill_name",
)


def to_skill_name(node):
    """
    read a corpus node's title and convert it to a kebab-case skill name

    the title is taken from the node's ``display_name``; every run of
    characters outside ``[a-z0-9]`` collapses to a single hyphen and
    leading/trailing hyphens are stripped, so the result matches
    Anthropic's skill-name grammar
    ``^[a-z0-9]([a-z0-9]|-[a-z0-9])*$`` -- a title such as
    ``Abbr Starts with Digits 0~9`` yields ``abbr-starts-with-digits-0-9``
    rather than an upload-rejected slug containing ``~``


    :param node: object exposing a ``display_name`` title, such as a
            ``BlueprintRegistry`` or ``ExportableAbbr``
    :type node: object
    :return: lowercase, hyphen-separated skill name
    :rtype: str
    """
    return re.sub(r"[^a-z0-9]+", "-", node.display_name.lower()).strip("-")


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

    @property
    def skill_name(self):
        """
        :return: canonical kebab-case skill name from ``display_name``
        :rtype: str
        """
        return to_skill_name(self)


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
