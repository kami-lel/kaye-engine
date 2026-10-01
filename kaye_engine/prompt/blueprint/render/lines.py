"""
render.lines.py

define:

- ``render_prompt_lines``
- ``render_negative_prompt_lines``
"""

from ...prompt_corpus_node import HEADING_PREFIX_ELEMENT
from ...sidecar_node import AVOID_NAME
from ..render_mode import RenderMode
from ..render_profile import RenderProfile
from .sidecar_splice import splice_sidecars
from .comment import render_comment_lines
from .util import apply_sparseness

__all__ = (
    "render_negative_prompt_lines",
    "render_prompt_lines",
)


def _join_blocks(blocks):
    """
    :return: ``blocks`` concatenated, each separated by one blank line
    :rtype: list[str]
    """
    lines = []
    for block in blocks:
        if lines:
            lines.append("")
        lines.extend(block)
    return lines


def _remove_first_heading_line(lines):
    """
    :return: ``lines`` with its first markdown heading line (if any)
            removed
    :rtype: list[str]
    """
    prefix = HEADING_PREFIX_ELEMENT
    for i, line in enumerate(lines):
        stripped = line.lstrip(prefix)
        prefix_len = len(line) - len(stripped)
        if prefix_len and stripped.startswith(" "):
            return lines[:i] + lines[i + 1 :]
    return lines


def _flatten_headings_for_image_mode(lines):
    """
    rewrite every markdown heading line (``### title``) to a bare
    ``title:`` line, regardless of nesting depth; non-heading lines
    pass through unchanged

    (helper function used in ``render_prompt_lines()`` and
    ``render_negative_prompt_lines()`` when ``RenderMode.IMAGE`` is set)


    :param lines:
    :type lines: list[str]
    :return: lines with every heading flattened
    :rtype: list[str]
    """
    prefix = HEADING_PREFIX_ELEMENT
    result = []
    for line in lines:
        stripped = line.lstrip(prefix)
        prefix_len = len(line) - len(stripped)
        if prefix_len and stripped.startswith(" "):
            result.append(stripped[1:] + ":")
        else:
            result.append(line)
    return result


def _resolve_is_comment_compact(profile, is_comment_compact):
    """
    :return: ``is_comment_compact``, or ``profile.sparseness == -1`` when
            ``None``
    :rtype: bool
    """
    if is_comment_compact is None:
        return profile.sparseness == -1
    return is_comment_compact


def _walk_set_bits(mask):
    """
    :return: positions of the set bits of ``mask``, ascending -- which is
            pre-order, so no sorting is needed
    :rtype: Iterator[int]
    """
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def _render_dynamic_block(index, idx, **kwargs):
    """
    :return: heading line then live content lines of dynamic node
            ``idx``, whose content depends on render options
    :rtype: tuple[str, ...]
    """
    node = index.node_objs[idx]
    return (
        HEADING_PREFIX_ELEMENT * node.depth + " " + node.name,
        *node.content_lines(**kwargs),
    )


def _iter_idxs_pre_order(index, idx, reverse_sibling_order):
    """
    :return: ``idx`` and its descendants' positions in pre-order, the
            siblings of every level reversed when ``reverse_sibling_order``
    :rtype: Iterator[int]
    """
    yield idx
    children = index.child_idxs[idx]
    for child_idx in reversed(children) if reverse_sibling_order else children:
        yield from _iter_idxs_pre_order(index, child_idx, reverse_sibling_order)


def _render_post_order_recursively(
    selection, idx, *, reverse_sibling_order=False, **kwargs
):
    """
    recursively render node ``idx`` and its descendants with every
    child's block first (children kept in original relative order, or
    reversed when ``reverse_sibling_order`` is set), then this node's own
    heading and content last

    (helper function used in ``render_prompt_lines()`` when
    ``RenderMode.POST_ORDER`` is set)


    :param selection:
    :type selection: BlueprintSelection
    :param idx: position of the node to render
    :type idx: int
    :param reverse_sibling_order: whether to reverse sibling order at
            every level of the walk
    :type reverse_sibling_order: bool
    :param kwargs: further render options forwarded to each selected
            dynamic node's ``content_lines(**kwargs)``
    :return: rendered lines for the node and its descendants, or an
            empty list when nothing in this subtree is selected
    :rtype: list[str]
    """
    index = selection.index

    children = index.child_idxs[idx]
    child_blocks = []
    for child_idx in reversed(children) if reverse_sibling_order else children:
        block = _render_post_order_recursively(
            selection,
            child_idx,
            reverse_sibling_order=reverse_sibling_order,
            **kwargs,
        )
        if block:
            child_blocks.append(block)

    blocks = list(child_blocks)
    if selection.mask >> idx & 1:
        blocks.append(
            list(
                index.blocks[idx]
                or _render_dynamic_block(index, idx, **kwargs)
            )
        )

    return _join_blocks(blocks)


def render_prompt_lines(
    selection,
    *,
    profile=RenderProfile(),
    is_comment_compact=None,
    **kwargs,
):
    """
    generate prompt as a list of lines from ``selection``

    optionally splices conditional sidecar nodes of specified name(s)
    into the selection before rendering.


    :param selection: nodes to render, dependencies already resolved
    :type selection: BlueprintSelection
    :param profile: bundled render settings -- see `RenderProfile` for
            the full field list (``show_comment``,
            ``disable_first_heading``, ``conditional_sidecars``,
            ``variants``, ``display_name``, ``sparseness``, ``mode``,
            plus the glossary-related fields); defaults to a plain
            `RenderProfile()`
    :type profile: RenderProfile, optional
    :param is_comment_compact: whether to render the comment as one line;
            ``None`` derives it from ``profile.sparseness == -1``
    :type is_comment_compact: bool, optional
    :param kwargs: further render options (e.g. ``query``) forwarded
            to each selected dynamic node's ``content_lines(**kwargs)``
    :return: list of prompt lines
    :rtype: list[str]
    """
    selection = splice_sidecars(
        selection,
        conditional_sidecars=profile.conditional_sidecars,
        variants=profile.variants,
    )
    index = selection.index

    reverse_sibling_order = RenderMode.REVERSE_ORDER in profile.mode

    if RenderMode.POST_ORDER in profile.mode:
        lines = _render_post_order_recursively(
            selection,
            0,
            reverse_sibling_order=reverse_sibling_order,
            **kwargs,
        )
        if profile.disable_first_heading:
            lines = _remove_first_heading_line(lines)
    else:
        lines = []
        should_skip_heading = profile.disable_first_heading
        node_cnt = len(index.node_objs)

        if reverse_sibling_order:
            # the last node walked, not the last in corpus order, gets no
            # blank line after it
            walk = (
                (pos, idx)
                for pos, idx in enumerate(
                    _iter_idxs_pre_order(index, 0, True)
                )
                if selection.mask >> idx & 1
            )
        else:
            walk = ((idx, idx) for idx in _walk_set_bits(selection.mask))

        for pos, idx in walk:
            block = index.blocks[idx] or _render_dynamic_block(
                index, idx, **kwargs
            )

            if should_skip_heading:
                should_skip_heading = False
            else:
                lines.append(block[0])

            # a blank line follows content, except after the last node
            if len(block) > 1:
                lines.extend(block[1:])
                if pos != node_cnt - 1:
                    lines.append("")

    if RenderMode._IMAGE in profile.mode:
        lines = _flatten_headings_for_image_mode(lines)

    # appended last, so a registered line starting with "#" stays untouched
    if profile.show_comment:
        lines.extend(
            render_comment_lines(
                profile.display_name,
                is_compact=_resolve_is_comment_compact(
                    profile, is_comment_compact
                ),
            )
        )

    return apply_sparseness(lines, profile.sparseness)


def _render_negative_node_recursively(
    selection,
    idx,
    *,
    avoid_mask,
    sidecar_mask,
    is_post_order,
    reverse_sibling_order,
    is_title_shown,
    **kwargs,
):
    """
    recursively render one node's contribution to a negative prompt

    a node's own ``{avoid}`` sidecar child contributes only when the
    node itself is selected; descendants are always walked regardless of
    this node's own selection, so a selected descendant several levels
    below an unselected ancestor still contributes. A node with no
    ``{avoid}`` content of its own is transparent: its contributing
    descendants' blocks splice in directly, with no heading of this
    node's own -- a node contributes at all only when it, or some
    descendant, carries ``{avoid}`` content; a node with neither is
    omitted entirely, and non-``avoid`` sidecar children
    (``{description}``, ``{when_to_use}``, ...) never contribute

    (helper function used in ``render_negative_prompt_lines()``)


    :param selection:
    :type selection: BlueprintSelection
    :param idx: position of the node to render, never the corpus root
    :type idx: int
    :param avoid_mask: node mask of every ``{avoid}`` sidecar
    :type avoid_mask: int
    :param sidecar_mask: node mask of every sidecar
    :type sidecar_mask: int
    :param is_post_order: whether this node's own block follows its
            children's rather than precedes them
    :type is_post_order: bool
    :param reverse_sibling_order: whether to reverse sibling order at
            every level of the walk
    :type reverse_sibling_order: bool
    :param is_title_shown: whether to print each contributing node's own
            heading above its ``{avoid}`` content
    :type is_title_shown: bool
    :param kwargs: further render options forwarded to the ``{avoid}``
            node's ``content_lines(**kwargs)``
    :return: rendered lines for the node and its descendants, or an
            empty list when nothing in this subtree contributes
    :rtype: list[str]
    """
    index = selection.index
    is_selected = selection.mask >> idx & 1

    own_avoid_lines = []
    child_blocks = []

    children = index.child_idxs[idx]
    for child_idx in reversed(children) if reverse_sibling_order else children:
        if avoid_mask >> child_idx & 1:
            if is_selected:
                block = index.blocks[child_idx]
                own_avoid_lines = list(
                    block[1:]
                    if block is not None
                    else index.node_objs[child_idx].content_lines(**kwargs)
                )
        elif not sidecar_mask >> child_idx & 1:
            block = _render_negative_node_recursively(
                selection,
                child_idx,
                avoid_mask=avoid_mask,
                sidecar_mask=sidecar_mask,
                is_post_order=is_post_order,
                reverse_sibling_order=reverse_sibling_order,
                is_title_shown=is_title_shown,
                **kwargs,
            )
            if block:
                child_blocks.append(block)

    if not own_avoid_lines:
        return _join_blocks(child_blocks)

    own_lines = []
    if is_title_shown:
        own_lines.append(index.blocks[idx][0])
    own_lines.extend(own_avoid_lines)

    if is_post_order:
        return _join_blocks(child_blocks + [own_lines])
    return _join_blocks([own_lines] + child_blocks)


def render_negative_prompt_lines(
    selection,
    *,
    profile=RenderProfile(),
    is_comment_compact=None,
    **kwargs,
):
    """
    generate **negative prompt** as a list of lines from ``selection``

    walks every node of the corpus; a selected node's own ``{avoid}``
    sidecar child supplies its printed content (that child's own heading
    is never shown), and a node is printed at all only when it or some
    descendant carries ``{avoid}`` content -- branches with none are
    omitted entirely. A node with no ``{avoid}`` content of its own, but
    a contributing descendant, is transparent: its own heading is never
    printed either, only the descendant's

    when ``profile.mode`` contains both ``RenderMode.NEGATIVE`` and
    ``RenderMode.IMAGE``, no node's own heading is printed at all, at
    any depth -- only the ``{avoid}`` content itself remains, its
    blocks still separated by one blank line


    :param selection: nodes to render, dependencies already resolved
    :type selection: BlueprintSelection
    :param profile: bundled render settings -- of `RenderProfile`'s
            fields, only ``conditional_sidecars``, ``variants``,
            ``show_comment``, ``display_name``, ``sparseness``, and
            ``mode`` apply here; defaults to a plain `RenderProfile()`
    :type profile: RenderProfile, optional
    :param is_comment_compact: whether to render the comment as one line;
            ``None`` derives it from ``profile.sparseness == -1``
    :type is_comment_compact: bool, optional
    :param kwargs: further render options forwarded to each ``{avoid}``
            node's ``content_lines(**kwargs)``
    :return: list of negative-prompt lines
    :rtype: list[str]
    """
    selection = splice_sidecars(
        selection,
        conditional_sidecars=profile.conditional_sidecars,
        variants=profile.variants,
    )
    index = selection.index

    sidecar_mask = 0
    for name_mask in index.sidecar_masks.values():
        sidecar_mask |= name_mask

    reverse_sibling_order = RenderMode.REVERSE_ORDER in profile.mode

    # image-mode negative prompt carries bare content, no titles
    mode = profile.mode
    is_title_shown = not (
        RenderMode.NEGATIVE in mode and RenderMode._IMAGE in mode
    )

    child_blocks = []
    root_children = index.child_idxs[0]
    for child_idx in (
        reversed(root_children) if reverse_sibling_order else root_children
    ):
        block = _render_negative_node_recursively(
            selection,
            child_idx,
            avoid_mask=index.sidecar_masks.get(AVOID_NAME, 0),
            sidecar_mask=sidecar_mask,
            is_post_order=RenderMode.POST_ORDER in mode,
            reverse_sibling_order=reverse_sibling_order,
            is_title_shown=is_title_shown,
            **kwargs,
        )
        if block:
            child_blocks.append(block)
    lines = _join_blocks(child_blocks)

    if RenderMode._IMAGE in mode:
        lines = _flatten_headings_for_image_mode(lines)

    # appended last, so a registered line starting with "#" stays untouched
    if profile.show_comment:
        lines.extend(
            render_comment_lines(
                profile.display_name,
                is_compact=_resolve_is_comment_compact(
                    profile, is_comment_compact
                ),
            )
        )

    return apply_sparseness(lines, profile.sparseness)
