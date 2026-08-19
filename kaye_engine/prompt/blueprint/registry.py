"""
registry.py

define `BlueprintRegistry`, `register_blueprint`, `blueprint_registry`
"""

from dataclasses import dataclass

from kaye_engine.exportable import (
    Exportable,
    merge_affordances,
    merge_conditional_sidecars,
    register_exportable_entry,
)

from .prompt_blueprint import PromptBlueprint

__all__ = (
    "BlueprintRegistry",
    "blueprint_registry",
    "get_blueprint",
    "register_blueprint",
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
    :param is_exportable: whether this blueprint is exported as a Claude
            Agent Skill; defaults to True
    :type is_exportable: bool, optional
    """

    blueprint: PromptBlueprint
    is_exportable: bool = True

    def content(self, **kwargs):
        """
        :param kwargs: render options forwarded to
                ``PromptBlueprint.generate_prompt(...)``; ``conditional_sidecars``
                and ``affordances`` default to this registry entry's own
                values unless passed explicitly
        :return: this blueprint's rendered prompt
        :rtype: str
        """
        kwargs.setdefault("conditional_sidecars", self.conditional_sidecars)
        kwargs.setdefault("affordances", self.affordances)
        return self.blueprint.generate_prompt(**kwargs)

    def merge(self, other):
        """
        create a new, unregistered `BlueprintRegistry` combining
        ``self`` and ``other``: the underlying blueprints are merged
        via ``|``, ``conditional_sidecars``/``affordances`` are merged
        via :func:`merge_conditional_sidecars`/:func:`merge_affordances`;
        every other field (``canonical_name``, ``display_name``,
        ``is_exportable``, ``always_apply``, ``user_invokable``,
        ``llm_invokable``) is taken from ``self``


        :param other: registry entry to merge with
        :type other: BlueprintRegistry
        :raises TypeError: ``other`` is not a `BlueprintRegistry`
        :return: newly created, unregistered merged entry
        :rtype: BlueprintRegistry
        """
        if not isinstance(other, BlueprintRegistry):
            raise TypeError(
                "cannot merge BlueprintRegistry with {}".format(type(other))
            )

        return BlueprintRegistry(
            canonical_name=self.canonical_name,
            display_name=self.display_name,
            blueprint=self.blueprint | other.blueprint,
            is_exportable=self.is_exportable,
            always_apply=self.always_apply,
            user_invokable=self.user_invokable,
            llm_invokable=self.llm_invokable,
            conditional_sidecars=merge_conditional_sidecars(
                self.conditional_sidecars, other.conditional_sidecars
            ),
            affordances=merge_affordances(
                self.affordances, other.affordances
            ),
        )


# Entry Point  #################################################################

blueprint_registry = {}


def register_blueprint(
    canonical_name,
    display_name,
    blueprint,
    *,
    is_exportable=True,
    always_apply=False,
    user_invokable=True,
    llm_invokable=True,
    conditional_sidecars=(),
    affordances=None,
):
    """
    create a `BlueprintRegistry` and insert it into `blueprint_registry`;
    when ``is_exportable``, the same instance is also inserted into
    `exportable_registry` via `register_exportable_entry`


    :param canonical_name: kebab-case name, used directly as the
            exported skill name when ``is_exportable``
    :type canonical_name: str
    :param display_name: human-readable name, e.g. ``"Coder Python"``
    :type display_name: str
    :param blueprint: the underlying blueprint
    :type blueprint: PromptBlueprint
    :param is_exportable: whether this blueprint is exported as a Claude
            Agent Skill; defaults to True
    :type is_exportable: bool, optional
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
    :param conditional_sidecars: used as the default collection of
            conditional sidecar node names to auto-checkmark unless the
            caller passes its own value explicitly; defaults to ``()``
            (disabled)
    :type conditional_sidecars: Iterable[str], optional
    :param affordances: used as the default per-``affordance_registry``
            checkmark selection unless the caller passes its own value
            explicitly; ``None`` passes off (default), ``()`` passes on
            with every affordance unavailable
    :type affordances: Iterable[str] or None, optional
    :raises ValueError: ``canonical_name`` is already registered
    :return: the created registry entry
    :rtype: BlueprintRegistry
    :example:
    >>> register_blueprint("coder", "Kaye Peer Coder", coder_blueprint, always_apply=True)
    >>> register_blueprint("chat", "Chat", chat_blueprint, is_exportable=False)
    """
    if canonical_name in blueprint_registry:
        raise ValueError(
            "duplicate blueprint registry name: {}".format(canonical_name)
        )

    reg = BlueprintRegistry(
        canonical_name=canonical_name,
        display_name=display_name,
        blueprint=blueprint,
        is_exportable=is_exportable,
        always_apply=always_apply,
        user_invokable=user_invokable,
        llm_invokable=llm_invokable,
        conditional_sidecars=conditional_sidecars,
        affordances=affordances,
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
