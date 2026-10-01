"""
render.sidecar_splice.py

define ``splice_sidecars`` and, until the renderers move to selections,
``_splice_conditional_sidecars``
"""

import copy

from anytree import PreOrderIter

from ...sidecar_node import get_sidecar_name

from ..index import BlueprintSelection

__all__ = ("_splice_conditional_sidecars", "splice_sidecars")


def _build_variant_sidecar_map(variants):
    """
    build a sidecar-name -> should-checkmark lookup: one ``Usage``/
    ``Lack`` entry pair per ``variant_registry`` entry, checkmarked on
    presence/absence in ``variants``, and one ``Usage``/``Fallback``
    entry pair per ``affordance_registry`` entry, checkmarked when
    any/none of its registered variants are present in ``variants``

    (helper function used in ``_splice_conditional_sidecars()``)


    :param variants: canonical names of variants available on the
            target surface
    :type variants: collections.abc.Iterable[str]
    :return: sidecar name -> whether it should be auto-checkmarked
    :rtype: dict[str, bool]
    """
    from ...affordance_registry import affordance_registry, variant_registry

    available = set(variants)
    sidecar_map = {}

    variants_by_affordance = {}
    for entry in variant_registry.values():
        is_available = entry.canonical_name in available
        sidecar_map[entry.usage_sidecar_name] = is_available
        sidecar_map[entry.lack_sidecar_name] = not is_available
        variants_by_affordance.setdefault(entry.affordance_name, []).append(
            is_available
        )

    for affordance in affordance_registry.values():
        member_availabilities = variants_by_affordance.get(
            affordance.canonical_name, ()
        )
        sidecar_map[affordance.usage_sidecar_name] = any(member_availabilities)
        all_missing = bool(member_availabilities) and not any(
            member_availabilities
        )
        sidecar_map[affordance.fallback_sidecar_name] = all_missing

    return sidecar_map


def splice_sidecars(selection, *, conditional_sidecars, variants):
    """
    add the conditional sidecar nodes to ``selection``, as mask arithmetic
    on the index's ``sidecar_masks`` -- both plain ``conditional_sidecars``
    name matches and, when ``variants`` is given, the ``Usage``/``Lack``/
    ``Fallback`` sidecars derived from ``variant_registry`` and
    ``affordance_registry``; a sidecar is spliced in only when its parent
    is selected


    :param selection: the selection to splice into; left untouched
    :type selection: BlueprintSelection
    :param conditional_sidecars: sidecar names to splice in
    :type conditional_sidecars: collections.abc.Iterable[str]
    :param variants: canonical names of variants available on the target
            surface; ``None`` disables the variant mechanism
    :type variants: collections.abc.Iterable[str] or None
    :return: ``selection``, or a new selection with the sidecars spliced
            in when either mechanism has anything to apply
    :rtype: BlueprintSelection
    """
    variant_sidecar_names = (
        _build_variant_sidecar_map(variants) if variants is not None else None
    )

    if not conditional_sidecars and variant_sidecar_names is None:
        return selection

    index = selection.index
    wanted = 0
    for name, name_mask in index.sidecar_masks.items():
        if name in conditional_sidecars or (
            variant_sidecar_names is not None
            and variant_sidecar_names.get(name)
        ):
            wanted |= name_mask

    # ascending bit order is pre-order, so a sidecar nested under another
    # spliced sidecar sees its parent already added
    mask = selection.mask
    remaining = wanted
    while remaining:
        low = remaining & -remaining
        idx = low.bit_length() - 1
        remaining ^= low
        if mask >> index.parent_idxs[idx] & 1:
            mask |= low

    return BlueprintSelection(index, mask)


def _splice_conditional_sidecars(
    blueprint, *, conditional_sidecars, variants
):
    """
    auto-checkmark conditional sidecar nodes ahead of rendering -- both
    plain ``conditional_sidecars`` name matches and, when ``variants``
    is given, the ``Usage``/``Lack``/``Fallback`` sidecars derived
    from ``variant_registry``/``affordance_registry``

    (helper function used in ``render_prompt_lines()``)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param conditional_sidecars: see ``render_prompt_lines()``
    :type conditional_sidecars: collections.abc.Iterable[str]
    :param variants: see ``render_prompt_lines()``
    :type variants: collections.abc.Iterable[str] or None
    :return: ``blueprint``, or a checkmark-spliced copy of it when either
            mechanism has anything to apply
    :rtype: PromptBlueprint
    """
    variant_sidecar_names = (
        _build_variant_sidecar_map(variants) if variants is not None else None
    )

    if not conditional_sidecars and variant_sidecar_names is None:
        return blueprint

    working_bp = copy.copy(blueprint)
    for node in PreOrderIter(working_bp.corpus):
        sidecar_name = get_sidecar_name(node)
        if sidecar_name is None or not working_bp.is_checkmarked(node.parent):
            continue
        if sidecar_name in conditional_sidecars or (
            variant_sidecar_names is not None
            and variant_sidecar_names.get(sidecar_name)
        ):
            working_bp.checkmark(node)

    return working_bp
