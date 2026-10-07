"""
select.py

define ``select_exportables``
"""

from kaye_engine.exportable import exportable_registry

__all__ = ("select_exportables",)


# Public API  ##################################################################
def select_exportables(names=None):
    """
    pick the `exportable_registry` entries to export as skills

    resolves every name before returning, so a bad name never leaves a
    partial selection behind; a repeated name is selected once


    :param names: canonical names to select; ``None`` selects every entry
    :type names: Iterable[str], optional
    :raises ValueError: 1+ names are not registered; the message lists
            every unknown name
    :return: selected entries, in the order named (registry order when
            ``names`` is ``None``)
    :rtype: list[Exportable]
    :example:
    >>> select_exportables(["coder", "chat"])
    """
    if names is None:
        return list(exportable_registry.values())

    unique_names = list(dict.fromkeys(names))
    unknown = [n for n in unique_names if n not in exportable_registry]
    if unknown:
        raise ValueError("unknown skill name: " + ", ".join(unknown))

    return [exportable_registry[n] for n in unique_names]
