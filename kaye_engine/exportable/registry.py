"""
registry.py

define ``exportable_registry``, ``register_exportable_entry``,
``get_exportable``
"""

__all__ = (
    "exportable_registry",
    "register_exportable_entry",
    "get_exportable",
)

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
