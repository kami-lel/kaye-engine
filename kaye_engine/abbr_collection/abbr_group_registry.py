"""
abbr_group_registry.py

define ``AbbrGroupRegistry``, ``register_abbr_group``, ``abbr_group_registry``
"""

from dataclasses import dataclass

__all__ = (
    "AbbrGroupRegistry",
    "abbr_group_registry",
    "get_abbr_group",
    "register_abbr_group",
)


@dataclass
class AbbrGroupRegistry:
    """
    metadata for a single, consumer-defined abbr **group**

    instances are created via `register_abbr_group` and collected in
    `abbr_group_registry`; this is the single source of truth for
    whether an `AbbrEntry.groups` name is known, and how its
    :class:`AbbrGroupNode` renders by default


    :param name: canonical group name, as it appears in
            ``AbbrEntry.groups`` and in the ``(name)`` corpus heading
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

abbr_group_registry = {}


def register_abbr_group(
    name, uses_numbered_list=False, is_sorted=False, priority_threshold=None
):
    """
    create an `AbbrGroupRegistry` and insert it into `abbr_group_registry`

    every group name an :class:`AbbrEntry` may declare via its
    ``groups`` field must be registered here first; adding an entry
    that references an unregistered group raises ``ValueError``


    :param priority_threshold: see :class:`AbbrGroupRegistry`
    :type priority_threshold: int, optional
    :raise ValueError: ``name`` is already registered
    :raise TypeError: ``priority_threshold`` is neither ``None`` nor
            an ``int``
    :return: the created registry entry
    :rtype: AbbrGroupRegistry
    """
    if name in abbr_group_registry:
        raise ValueError("duplicate abbr group registry name: {}".format(name))
    if priority_threshold is not None and not isinstance(
        priority_threshold, int
    ):
        raise TypeError(
            "priority_threshold must be an int or None, got: {}".format(
                type(priority_threshold)
            )
        )

    reg = AbbrGroupRegistry(
        name, uses_numbered_list, is_sorted, priority_threshold
    )
    abbr_group_registry[name] = reg

    return reg


def get_abbr_group(name):
    """
    :param name: canonical string key a group was registered under via
            `register_abbr_group`
    :type name: str
    :raises KeyError: no group is registered under ``name``
    :return: the registry entry stored under ``name``
    :rtype: AbbrGroupRegistry
    """
    try:
        return abbr_group_registry[name]
    except KeyError as e:
        raise KeyError(
            "no abbr group registered under name: {}".format(name)
        ) from e
