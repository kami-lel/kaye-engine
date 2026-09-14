"""
comfy_ui_export.py

define ``comfy_ui_exportable_registry``, ``register_comfy_ui_exportable``
"""

from .registry import get_exportable

__all__ = (
    "comfy_ui_exportable_registry",
    "register_comfy_ui_exportable",
)

comfy_ui_exportable_registry = []


def register_comfy_ui_exportable(canonical_name):
    """
    mark ``canonical_name`` as a member of the ComfyUI export subset

    ``canonical_name`` must already be registered in `exportable_registry`;
    this call never creates or registers an exportable itself


    :param canonical_name: canonical name an exportable was registered
            under via `register_exportable_entry`
    :type canonical_name: str
    :raises KeyError: no exportable is registered under ``canonical_name``
    :raises ValueError: ``canonical_name`` is already in the subset
    :return: ``canonical_name``, unchanged
    :rtype: str
    :example:
    >>> register_comfy_ui_exportable("redact-photo-for-privacy")
    """
    get_exportable(canonical_name)

    if canonical_name in comfy_ui_exportable_registry:
        raise ValueError(
            "duplicate comfy-ui exportable registry name: {}".format(
                canonical_name
            )
        )

    comfy_ui_exportable_registry.append(canonical_name)

    return canonical_name
