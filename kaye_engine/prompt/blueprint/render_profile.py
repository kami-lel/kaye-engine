"""
render_profile.py

define ``RenderProfile``
"""

import dataclasses
from dataclasses import dataclass

__all__ = ("RenderProfile",)


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


def merge_variants(*selections):
    """
    union of variant selections across ``selections``, deduped,
    first-seen order; ``None`` means "off" and contributes nothing


    :param selections: variant selections to merge
    :type selections: Iterable[str] or None
    :return: merged, deduped variant selection; ``None`` only when
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


@dataclass(kw_only=True)
class RenderProfile:
    """
    named, layerable bundle of render kwargs threaded through
    ``render_prompt_lines`` / ``generate_prompt_without_dependencies`` /
    ``BlueprintRegistry.content`` -- ``.merge()`` overrides scalar fields
    and unions the collection fields


    :param show_comment: show comment part after last line;
            defaults to False
    :type show_comment: bool, optional
    :param disable_first_heading: whether disable showing top heading;
            defaults to False
    :type disable_first_heading: bool, optional
    :param conditional_sidecars: auto-checkmark conditional sidecar nodes
            whose name is in this collection and whose parent is
            checkmarked; defaults to ``()`` (disabled)
    :type conditional_sidecars: Iterable[str], optional
    :param variants: canonical names present here checkmark their
            ``Usage`` node; an affordance whose variants are all
            absent checkmarks its ``Fallback`` node instead. ``None``:
            off (default). ``()``: on, everything absent.
    :type variants: Iterable[str] or None, optional
    :param display_name: blueprint's human-readable name, included in
            the comment when ``show_comment`` is set; defaults to ""
    :type display_name: str, optional
    :param sparseness: controls how runs of blank lines collapse;
            defaults to 1
    :type sparseness: int, optional
    :param glossary_priority_threshold: forwarded to
            ``GlossaryNode.content_lines()``; defaults to None
    :type glossary_priority_threshold: int, optional
    :param is_sorted: forwarded to ``GlossaryNode.content_lines()``;
            defaults to None
    :type is_sorted: bool, optional
    :param is_numbered_list: forwarded to
            ``GlossaryNode.content_lines()``; defaults to None
    :type is_numbered_list: bool, optional
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
        merged.conditional_sidecars = merge_conditional_sidecars(
            self.conditional_sidecars, other.conditional_sidecars
        )
        merged.variants = merge_variants(self.variants, other.variants)
        return merged
