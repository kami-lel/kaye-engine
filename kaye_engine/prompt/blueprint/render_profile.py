"""
render_profile.py

define ``RenderProfile``
"""

import dataclasses
from dataclasses import dataclass

from .render_mode import RenderMode

__all__ = ("RenderProfile",)


def _merge_conditional_sidecars(*groups):
    """
    :return: union of sidecar names across ``groups``, deduped,
            first-seen order
    :rtype: tuple
    """
    merged = []
    for group in groups:
        for name in group:
            if name not in merged:
                merged.append(name)
    return tuple(merged)


def _merge_variants(*selections):
    """
    :return: union of variant selections across ``selections``, deduped,
            first-seen order; ``None`` means "off" and contributes
            nothing, and is returned only when every selection is
            ``None``
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


@dataclass(kw_only=True)
class RenderProfile:
    """
    named, layerable bundle of render settings

    ※ `Render Profile Documentation <../../../docs/render-profile-doc.md>`__
    """

    show_comment: bool = False
    disable_first_heading: bool = False
    conditional_sidecars: tuple = ()
    variants: object = None
    display_name: str = ""
    sparseness: int = 1
    glossary_priority_threshold: int = None
    is_sorted: bool = None
    is_numbered_list: bool = None
    mode: RenderMode = RenderMode.NORMAL

    def as_kwargs(self):
        """
        :return: this profile's fields as a splattable kwargs dict
        :rtype: dict
        """
        return dataclasses.asdict(self)

    def merge(self, other):
        """
        combine ``self`` with ``other`` into a new instance -- ``other``
        wins for every scalar field; ``conditional_sidecars`` and
        ``variants`` union instead of override


        :param other: profile to merge with
        :type other: RenderProfile
        :return: newly created merged instance
        :rtype: RenderProfile
        """
        merged = dataclasses.replace(other)
        merged.conditional_sidecars = _merge_conditional_sidecars(
            self.conditional_sidecars, other.conditional_sidecars
        )
        merged.variants = _merge_variants(self.variants, other.variants)
        return merged
