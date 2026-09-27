"""
image_prompt_export.py

define ``image_prompt_exportable_registry``,
``register_image_prompt_exportable``
"""

from .registry import get_exportable

__all__ = (
    "image_prompt_exportable_registry",
    "register_image_prompt_exportable",
)

image_prompt_exportable_registry = []


def register_image_prompt_exportable(canonical_name):
    """
    mark ``canonical_name`` as a member of the image-prompt export subset

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
    >>> register_image_prompt_exportable("redact-photo-for-privacy")
    """
    get_exportable(canonical_name)

    if canonical_name in image_prompt_exportable_registry:
        raise ValueError(
            "duplicate image-prompt exportable registry name: {}".format(
                canonical_name
            )
        )

    image_prompt_exportable_registry.append(canonical_name)

    return canonical_name
