"""
exportable.py

define ``Exportable``, ``exportable_registry``,
``register_exportable_entry``, ``get_exportable``
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

__all__ = (
    "Exportable",
    "exportable_registry",
    "register_exportable_entry",
    "get_exportable",
)


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

    canonical_name: str
    display_name: str
    always_apply: bool = False
    user_invokable: bool = True
    llm_invokable: bool = True

    @abstractmethod
    def content(self):
        """
        generic, non-Claude-specific displayable content -- e.g. the
        rendered prompt for a blueprint, or the markdown abbr list for
        an abbr group; used by the ``kaye-engine export`` CLI command


        :return: this exportable's content
        :rtype: str
        """


# Entry Point  #################################################################

exportable_registry = {}


def register_exportable_entry(exportable):
    """
    insert ``exportable`` into `exportable_registry` under its
    `canonical_name`


    :param exportable: entry to register
    :type exportable: Exportable
    :raises ValueError: `canonical_name` is already registered
    :return: ``exportable``, unchanged
    :rtype: Exportable
    :example:
    >>> register_exportable_entry(my_exportable)
    """
    if exportable.canonical_name in exportable_registry:
        raise ValueError(
            "duplicate exportable registry name: {}".format(
                exportable.canonical_name
            )
        )

    exportable_registry[exportable.canonical_name] = exportable

    return exportable


def get_exportable(canonical_name):
    """
    :param canonical_name: canonical name an exportable was registered
            under via `register_exportable_entry`
    :type canonical_name: str
    :raises KeyError: no exportable is registered under ``canonical_name``
    :return: the registry entry stored under ``canonical_name``
    :rtype: Exportable
    :example:
    >>> get_exportable("coder")
    """
    try:
        return exportable_registry[canonical_name]
    except KeyError as e:
        raise KeyError(
            "no exportable registered under name: {}".format(canonical_name)
        ) from e
