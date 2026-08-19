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
    "merge_conditional_sidecars",
    "merge_affordances",
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
    :param conditional_sidecars: used as the default collection of
            conditional sidecar node names to auto-checkmark (e.g.,
            ``("Claude Tool:TodoWrite",)``) unless the caller passes its
            own value explicitly; defaults to ``()`` (disabled)
    :type conditional_sidecars: Iterable[str], optional
    :param affordances: used as the default per-``affordance_registry``
            checkmark selection unless the caller passes its own value
            explicitly; ``None`` passes off (default), ``()`` passes on
            with every affordance unavailable
    :type affordances: Iterable[str] or None, optional
    """

    canonical_name: str
    display_name: str
    user_invokable: bool = True
    llm_invokable: bool = True

    # hack hack leftover from an earlier attempt at generating a Continue AI
    # rule file; unused by any current consumer
    always_apply: bool = False

    conditional_sidecars: tuple = ()
    affordances: object = None

    @abstractmethod
    def content(self, **kwargs):
        """
        generic, non-Claude-specific displayable content -- e.g. the
        rendered prompt for a blueprint, or the markdown abbr list for
        an abbr group; used by the ``kaye-engine exportable`` CLI
        command


        :param kwargs: render options forwarded to
                ``PromptBlueprint.generate_prompt(...)`` by
                implementers that render a blueprint; ignored by
                implementers that don't
        :return: this exportable's content
        :rtype: str
        """

    @abstractmethod
    def merge(self, other):
        """
        combine ``self`` with ``other`` of a compatible kind into a
        new, unregistered instance; a concrete class with no sensible
        merge raises


        :param other: exportable to merge with
        :type other: Exportable
        :raises TypeError: ``other`` is not a compatible kind
        :raises NotImplementedError: this kind has no defined merge
        :return: newly created, unregistered merged instance
        :rtype: Exportable
        """

    def __or__(self, other):
        """
        create a merged exportable

        (wrapper of and identical to ``.merge()``)


        :param other:
        :type other: Exportable
        :raises TypeError:
        :raises NotImplementedError:
        :return: merged exportable
        :rtype: Exportable
        """
        if not isinstance(other, Exportable):
            return NotImplemented

        return self.merge(other)


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


def merge_conditional_sidecars(*groups):
    """
    union of sidecar names across ``groups``, deduped, first-seen order


    :param groups: conditional sidecar tuples to merge
    :type groups: Iterable[str]
    :return: merged, deduped sidecar names
    :rtype: tuple
    """
    merged = []
    for group in groups:
        for name in group:
            if name not in merged:
                merged.append(name)
    return tuple(merged)


def merge_affordances(*selections):
    """
    union of affordance selections across ``selections``, deduped,
    first-seen order; ``None`` means "off" and contributes nothing


    :param selections: affordance selections to merge
    :type selections: Iterable[str] or None
    :return: merged, deduped affordance selection; ``None`` only when
            every selection is ``None``
    :rtype: tuple or None
    """
    merged = []
    seen_non_none = False
    for selection in selections:
        if selection is None:
            continue
        seen_non_none = True
        for name in selection:
            if name not in merged:
                merged.append(name)

    if not seen_non_none:
        return None

    return tuple(merged)
