"""
abbr_glossary_registry.py

define ``AbbrGlossaryRegistry``, ``register_abbr_glossary``,
``abbr_glossary_registry``
"""

from dataclasses import dataclass

__all__ = (
    "AbbrGlossaryRegistry",
    "abbr_glossary_registry",
    "get_abbr_glossary",
    "register_abbr_glossary",
)


@dataclass
class AbbrGlossaryRegistry:
    """
    metadata for a single, consumer-defined abbr **glossary**

    instances are created via `register_abbr_glossary` and collected in
    `abbr_glossary_registry`; this is the single source of truth for
    whether an `AbbrEntry.glossaries` name is known, and how its
    :class:`GlossaryNode` renders by default


    :param name: canonical glossary name, as it appears in
            ``AbbrEntry.glossaries`` and in the ``(name)`` corpus heading
    :type name: str
    :param is_exportable: whether this glossary is registered into the
            exportable registry
    :type is_exportable: bool
    :param user_invokable: whether a human may deliberately invoke this
            glossary's exportable group directly, e.g. as a skill;
            defaults to True, unlike the engine's fixed tag/wrap/
            starts-with abbr groups, which are always llm-only
    :type user_invokable: bool, optional
    :param uses_numbered_list: render entries with numbered markers
            (``"1. ..."``) instead of bullets (``"- ..."``) by default;
            defaults to False
    :type uses_numbered_list: bool, optional
    :param is_sorted: render entries ordered by ascending
            :attr:`AbbrEntry.priority` instead of insertion order by
            default; defaults to False
    :type is_sorted: bool, optional
    :param disable_remark: render entries without the ``(...)`` remark
            suffix by default; defaults to False
    :type disable_remark: bool, optional
    :param register_as_dynamic_substitution: whether this glossary is
            reachable via a ``(((name)))`` dynamic substitution
            placeholder; defaults to False
    :type register_as_dynamic_substitution: bool, optional
    """

    name: str
    is_exportable: bool
    user_invokable: bool = True
    uses_numbered_list: bool = False
    is_sorted: bool = False
    disable_remark: bool = False
    register_as_dynamic_substitution: bool = False


# Main Entry Point  ############################################################

abbr_glossary_registry = {}


def register_abbr_glossary(
    name,
    is_exportable,
    user_invokable=True,
    uses_numbered_list=False,
    is_sorted=False,
    disable_remark=False,
    register_as_dynamic_substitution=False,
):
    """
    create an `AbbrGlossaryRegistry` and insert it into
    `abbr_glossary_registry`

    every glossary name an :class:`AbbrEntry` may declare via its
    ``glossaries`` field must be registered here first; adding an entry
    that references an unregistered glossary raises ``ValueError``


    :param is_exportable: whether this glossary is registered into the
            exportable registry
    :type is_exportable: bool
    :param user_invokable: whether a human may deliberately invoke this
            glossary's exportable group directly; defaults to True
    :type user_invokable: bool, optional
    :raise ValueError: ``name`` is already registered
    :return: the created registry entry
    :rtype: AbbrGlossaryRegistry
    """
    if name in abbr_glossary_registry:
        raise ValueError(
            "duplicate abbr glossary registry name: {}".format(name)
        )

    reg = AbbrGlossaryRegistry(
        name,
        is_exportable,
        user_invokable,
        uses_numbered_list,
        is_sorted,
        disable_remark,
        register_as_dynamic_substitution,
    )
    abbr_glossary_registry[name] = reg

    return reg


def get_abbr_glossary(name):
    """
    :param name: canonical string key a glossary was registered under
            via `register_abbr_glossary`
    :type name: str
    :raises KeyError: no glossary is registered under ``name``
    :return: the registry entry stored under ``name``
    :rtype: AbbrGlossaryRegistry
    """
    try:
        return abbr_glossary_registry[name]
    except KeyError as e:
        raise KeyError(
            "no abbr glossary registered under name: {}".format(name)
        ) from e
