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
    :param uses_numbered_list: render entries with numbered markers
            (``"1. ..."``) instead of bullets (``"- ..."``) by default;
            defaults to False
    :type uses_numbered_list: bool, optional
    :param is_sorted: render entries ordered by ascending
            :attr:`AbbrEntry.priority` instead of insertion order by
            default; defaults to False
    :type is_sorted: bool, optional
    :param priority_threshold: when set, entries whose
            :attr:`AbbrEntry.priority` is greater than this value are excluded
            from rendering; ``None`` disables this filtering; defaults to
            None
    :type priority_threshold: int, optional
    """

    name: str
    uses_numbered_list: bool = False
    is_sorted: bool = False
    priority_threshold: int = None


# Entry Point  #################################################################

abbr_glossary_registry = {}


def register_abbr_glossary(
    name, uses_numbered_list=False, is_sorted=False, priority_threshold=None
):
    """
    create an `AbbrGlossaryRegistry` and insert it into
    `abbr_glossary_registry`

    every glossary name an :class:`AbbrEntry` may declare via its
    ``glossaries`` field must be registered here first; adding an entry
    that references an unregistered glossary raises ``ValueError``


    :param priority_threshold: see :class:`AbbrGlossaryRegistry`
    :type priority_threshold: int, optional
    :raise ValueError: ``name`` is already registered
    :raise TypeError: ``priority_threshold`` is neither ``None`` nor
            an ``int``
    :return: the created registry entry
    :rtype: AbbrGlossaryRegistry
    """
    if name in abbr_glossary_registry:
        raise ValueError(
            "duplicate abbr glossary registry name: {}".format(name)
        )
    if priority_threshold is not None and not isinstance(
        priority_threshold, int
    ):
        raise TypeError(
            "priority_threshold must be an int or None, got: {}".format(
                type(priority_threshold)
            )
        )

    reg = AbbrGlossaryRegistry(
        name, uses_numbered_list, is_sorted, priority_threshold
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
