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
    :param is_user_invokable: whether a human may deliberately invoke this
            glossary's exportable group directly, e.g. as a skill;
            defaults to True, unlike the engine's fixed tag/wrap/
            starts-with abbr groups, which are always llm-only
    :type is_user_invokable: bool, optional
    :param is_numbered_list: whether entries render with numbered
            markers (``"1. ..."``) instead of bullets (``"- ..."``);
            defaults to False
    :type is_numbered_list: bool, optional
    :param is_sorted: whether entries render ordered by ascending
            :attr:`AbbrEntry.priority` instead of insertion order;
            defaults to False
    :type is_sorted: bool, optional
    :param is_remark_disabled: whether entries render without the
            ``(...)`` remark suffix; defaults to False
    :type is_remark_disabled: bool, optional
    :param is_term_definition_forced: whether every entry renders as a
            term definition (``- {mean}``, no ``{abbr}:`` prefix),
            regardless of whether it carries the ``term_definition``
            tag; defaults to False
    :type is_term_definition_forced: bool, optional
    :param is_dyn_substitution: whether this glossary is
            reachable via a ``(((name)))`` dynamic substitution
            placeholder; defaults to False
    :type is_dyn_substitution: bool, optional
    """

    name: str
    is_exportable: bool
    is_user_invokable: bool = True
    is_numbered_list: bool = False
    is_sorted: bool = False
    is_remark_disabled: bool = False
    is_term_definition_forced: bool = False
    is_dyn_substitution: bool = False


# Main Entry Point  ############################################################

abbr_glossary_registry = {}


def register_abbr_glossary(
    name,
    is_exportable,
    is_user_invokable=True,
    is_numbered_list=False,
    is_sorted=False,
    is_remark_disabled=False,
    is_term_definition_forced=False,
    is_dyn_substitution=False,
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
    :param is_user_invokable: whether a human may deliberately invoke this
            glossary's exportable group directly; defaults to True
    :type is_user_invokable: bool, optional
    :param is_term_definition_forced: whether every entry renders as a
            term definition, regardless of its own ``term_definition``
            tag; defaults to False
    :type is_term_definition_forced: bool, optional
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
        is_user_invokable,
        is_numbered_list,
        is_sorted,
        is_remark_disabled,
        is_term_definition_forced,
        is_dyn_substitution,
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
