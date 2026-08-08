"""
registry.py

define `BlueprintRegistry`, `register_blueprint`, `blueprint_registry`
"""

import re

from dataclasses import dataclass

from .prompt_blueprint import PromptBlueprint

__all__ = (
    "BlueprintRegistry",
    "register_blueprint",
    "get_blueprint",
    "blueprint_registry",
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
    `blueprint_registry`; this is the single source of truth for a
    blueprint's identity (`name`/`display_name`) and where it should be
    exported (Claude skills) and how


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
    """

    name: str
    display_name: str
    blueprint: PromptBlueprint
    skill_exportable: bool = False
    always_apply: bool = False
    user_invokable: bool = True
    llm_invokable: bool = True

    @property
    def skill_name(self):
        """
        :return: canonical kebab-case skill name from ``display_name``
        :rtype: str
        """
        return to_skill_name(self)


# Entry Point  #################################################################

blueprint_registry = {}


def register_blueprint(name, *args, **kwargs):
    """
    create a `BlueprintRegistry` and insert it into `blueprint_registry`

    ``args``/``kwargs`` are forwarded as-is into `BlueprintRegistry`; see
    its docstring for the full field list


    :raise ValueError: ``name`` is already registered
    :return: the created registry entry
    :rtype: BlueprintRegistry
    """
    if name in blueprint_registry:
        raise ValueError("duplicate blueprint registry name: {}".format(name))

    reg = BlueprintRegistry(name, *args, **kwargs)
    blueprint_registry[name] = reg

    return reg


def get_blueprint(name):
    """
    :param name: canonical string key a blueprint was registered under
            via `register_blueprint`
    :type name: str
    :raises KeyError: no blueprint is registered under ``name``
    :return: the registry entry stored under ``name``
    :rtype: BlueprintRegistry
    """
    try:
        return blueprint_registry[name]
    except KeyError as e:
        raise KeyError(
            "no blueprint registered under name: {}".format(name)
        ) from e
