"""
render.lines.py

define:

- ``render_prompt_lines``
- ``render_negative_prompt_lines``
"""

from ...prompt_corpus_node import HEADING_PREFIX_ELEMENT
from ...sidecar_node import AVOID_NAME, get_sidecar_name
from ..render_mode import RenderMode
from ..render_profile import RenderProfile
from .sidecar_splice import _splice_conditional_sidecars, splice_sidecars
from .comment import render_comment_lines
from .util import apply_sparseness

__all__ = (
    "render_negative_prompt_lines",
    "render_prompt_lines",
)


def _iter_children(node, reverse_sibling_order):
    """
    :return: ``node.children``, reversed when ``reverse_sibling_order``
    :rtype: Iterable
    """
    return reversed(node.children) if reverse_sibling_order else node.children


def _iter_nodes_pre_order(node, reverse_sibling_order):
    """
    pre-order walk of ``node`` and its descendants, replacing
    ``anytree.PreOrderIter`` to allow reversing sibling order at every
    level
    """
    yield node
    for child in _iter_children(node, reverse_sibling_order):
        yield from _iter_nodes_pre_order(child, reverse_sibling_order)


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


def _render_negative_prompt_node_recursively(
    blueprint,
    node,
    *,
    reverse_sibling_order=False,
    is_title_shown=True,
    **kwargs,
):
    """
    recursively render one node's contribution to a negative prompt

    a node's own ``{avoid}`` sidecar child contributes only when the
    node itself is checkmarked; descendants are always walked
    regardless of this node's own checkmark, so a checkmarked
    descendant several levels below an unchecked ancestor still
    contributes. A node with no ``{avoid}`` content of its own is
    transparent: its contributing descendants' blocks splice in
    directly, with no heading of this node's own, even though the
    node is checkmarked and the walk still visits it -- a node
    contributes at all only when it, or some descendant, carries
    ``{avoid}`` content; a node with neither is omitted entirely, and
    non-``avoid`` sidecar children (``{description}``,
    ``{when_to_use}``, ...) never contribute

    (helper function used in ``render_negative_prompt_lines()``)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param node: node to render, never the corpus root
    :type node: BasePromptNode
    :param reverse_sibling_order: whether to reverse sibling order at
            every level of the walk
    :type reverse_sibling_order: bool
    :param is_title_shown: whether to print each contributing node's own
            heading above its ``{avoid}`` content
    :type is_title_shown: bool
    :param kwargs: further render options forwarded to the ``{avoid}``
            node's ``content_lines(**kwargs)``
    :return: rendered lines for ``node`` and its descendants, or an
            empty list when nothing in this subtree contributes
    :rtype: list[str]
    """
    is_checked = blueprint.is_checkmarked(node)

    own_avoid_lines = []
    child_blocks = []

    for child in _iter_children(node, reverse_sibling_order):
        sidecar_name = get_sidecar_name(child)
        if sidecar_name == AVOID_NAME:
            if is_checked:
                own_avoid_lines = child.content_lines(**kwargs)
        elif sidecar_name is None:
            block = _render_negative_prompt_node_recursively(
                blueprint,
                child,
                reverse_sibling_order=reverse_sibling_order,
                is_title_shown=is_title_shown,
                **kwargs,
            )
            if block:
                child_blocks.append(block)

    if not own_avoid_lines and not child_blocks:
        return []

    if not own_avoid_lines:
        return _join_blocks(child_blocks)

    own_lines = []
    if is_title_shown:
        own_lines.append(HEADING_PREFIX_ELEMENT * node.depth + " " + node.name)
    own_lines.extend(own_avoid_lines)

    return _join_blocks([own_lines] + child_blocks)


def _render_prompt_node_post_order_recursively(
    blueprint, node, *, reverse_sibling_order=False, **kwargs
):
    """
    recursively render one node's contribution for
    ``RenderMode.POST_ORDER``: every child's full subtree first (each
    following the same rule, siblings kept in original relative
    order, or reversed when ``reverse_sibling_order`` is set), then
    this node's own heading and content last, only when this node
    itself is checkmarked -- checkmarking is evaluated per-node,
    independent of any ancestor's, matching the flat pre-order walk
    this replaces

    (helper function used in ``render_prompt_lines()`` when
    ``RenderMode.POST_ORDER`` is set)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param node:
    :type node: BasePromptNode
    :param reverse_sibling_order: whether to reverse sibling order at
            every level of the walk
    :type reverse_sibling_order: bool
    :param kwargs: further render options forwarded to each
            checkmarked node's ``content_lines(**kwargs)``
    :return: rendered lines for ``node`` and its descendants, or an
            empty list when nothing in this subtree contributes
    :rtype: list[str]
    """
    child_blocks = []
    for child in _iter_children(node, reverse_sibling_order):
        block = _render_prompt_node_post_order_recursively(
            blueprint,
            child,
            reverse_sibling_order=reverse_sibling_order,
            **kwargs,
        )
        if block:
            child_blocks.append(block)

    own_lines = []
    if blueprint.is_checkmarked(node):
        own_lines.append(HEADING_PREFIX_ELEMENT * node.depth + " " + node.name)
        content_lines = node.content_lines(**kwargs)
        if content_lines:
            own_lines.extend(content_lines)

    if not child_blocks and not own_lines:
        return []

    blocks = list(child_blocks)
    if own_lines:
        blocks.append(own_lines)

    return _join_blocks(blocks)


def _render_negative_prompt_node_post_order_recursively(
    blueprint,
    node,
    *,
    reverse_sibling_order=False,
    is_title_shown=True,
    **kwargs,
):
    """
    (``RenderMode.POST_ORDER`` counterpart of
    ``_render_negative_prompt_node_recursively``) recursively render
    one node's contribution to a negative prompt, with every
    contributing child's block first (children kept in original
    relative order, or reversed when ``reverse_sibling_order`` is
    set), then this node's own heading and ``{avoid}`` content last

    a node's own ``{avoid}`` sidecar child contributes only when the
    node itself is checkmarked; descendants are always walked
    regardless of this node's own checkmark, so a checkmarked
    descendant several levels below an unchecked ancestor still
    contributes. A node with no ``{avoid}`` content of its own is
    transparent: its contributing children's blocks propagate up
    unchanged, with no heading of this node's own

    (helper function used in ``render_negative_prompt_lines()`` when
    ``RenderMode.POST_ORDER`` is set)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param node: node to render, never the corpus root
    :type node: BasePromptNode
    :param reverse_sibling_order: whether to reverse sibling order at
            every level of the walk
    :type reverse_sibling_order: bool
    :param is_title_shown: whether to print each contributing node's own
            heading above its ``{avoid}`` content
    :type is_title_shown: bool
    :param kwargs: further render options forwarded to the ``{avoid}``
            node's ``content_lines(**kwargs)``
    :return: rendered lines for ``node`` and its descendants, or an
            empty list when nothing in this subtree contributes
    :rtype: list[str]
    """
    is_checked = blueprint.is_checkmarked(node)

    own_avoid_lines = []
    child_blocks = []

    for child in _iter_children(node, reverse_sibling_order):
        sidecar_name = get_sidecar_name(child)
        if sidecar_name == AVOID_NAME:
            if is_checked:
                own_avoid_lines = child.content_lines(**kwargs)
        elif sidecar_name is None:
            block = _render_negative_prompt_node_post_order_recursively(
                blueprint,
                child,
                reverse_sibling_order=reverse_sibling_order,
                is_title_shown=is_title_shown,
                **kwargs,
            )
            if block:
                child_blocks.append(block)

    if not own_avoid_lines and not child_blocks:
        return []

    if not own_avoid_lines:
        return _join_blocks(child_blocks)

    own_lines = []
    if is_title_shown:
        own_lines.append(HEADING_PREFIX_ELEMENT * node.depth + " " + node.name)
    own_lines.extend(own_avoid_lines)

    return _join_blocks(child_blocks + [own_lines])


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


def _legacy_render_prompt_lines(
    blueprint,
    *,
    profile=RenderProfile(),
    is_comment_compact=None,
    **kwargs,
):
    """
    generate prompt as a list of lines from ``blueprint``

    optionally auto-checkmarks sidecar nodes of specified name(s) before
    rendering.


    :param blueprint:
    :type blueprint: PromptBlueprint
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
            to each checkmarked node's ``content_lines(**kwargs)``
    :return: list of prompt lines
    :rtype: list[str]
    """
    working_bp = _splice_conditional_sidecars(
        blueprint,
        conditional_sidecars=profile.conditional_sidecars,
        variants=profile.variants,
    )

    reverse_sibling_order = RenderMode.REVERSE_ORDER in profile.mode

    if RenderMode.POST_ORDER in profile.mode:
        lines = _render_prompt_node_post_order_recursively(
            working_bp,
            working_bp.corpus,
            reverse_sibling_order=reverse_sibling_order,
            **kwargs,
        )
        if profile.disable_first_heading:
            lines = _remove_first_heading_line(lines)
    else:
        lines = []

        should_skip_heading = profile.disable_first_heading

        last_node_idx = working_bp.corpus.size - 1
        nodes = _iter_nodes_pre_order(working_bp.corpus, reverse_sibling_order)
        for i, node in enumerate(nodes):
            if working_bp.is_checkmarked(node):
                if should_skip_heading:
                    should_skip_heading = False
                else:
                    # heading line
                    lines.append(
                        HEADING_PREFIX_ELEMENT * node.depth + " " + node.name
                    )

                # content lines
                content_lines = node.content_lines(**kwargs)
                if content_lines:
                    lines.extend(content_lines)
                    if i != last_node_idx:
                        lines.append("")  # add an empty line

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


def render_negative_prompt_lines(
    blueprint,
    *,
    profile=RenderProfile(),
    is_comment_compact=None,
    **kwargs,
):
    """
    generate **negative prompt** as a list of lines from ``blueprint``

    walks every checkmarked node in ``blueprint``; a node's own
    ``{avoid}`` sidecar child supplies its printed content (that
    child's own heading is never shown), and a node is printed at all
    only when it or some descendant carries ``{avoid}`` content --
    branches with none are omitted entirely. A node with no ``{avoid}``
    content of its own, but a contributing descendant, is transparent:
    its own heading is never printed either, only the descendant's

    when ``profile.mode`` contains both ``RenderMode.NEGATIVE`` and
    ``RenderMode.IMAGE``, no node's own heading is printed at all, at
    any depth -- only the ``{avoid}`` content itself remains, its
    blocks still separated by one blank line


    :param blueprint:
    :type blueprint: PromptBlueprint
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
    working_bp = _splice_conditional_sidecars(
        blueprint,
        conditional_sidecars=profile.conditional_sidecars,
        variants=profile.variants,
    )

    reverse_sibling_order = RenderMode.REVERSE_ORDER in profile.mode

    recurse = (
        _render_negative_prompt_node_post_order_recursively
        if RenderMode.POST_ORDER in profile.mode
        else _render_negative_prompt_node_recursively
    )

    # image-mode negative prompt carries bare content, no titles
    mode = profile.mode
    is_title_shown = not (
        RenderMode.NEGATIVE in mode and RenderMode._IMAGE in mode
    )

    child_blocks = []
    for child in _iter_children(working_bp.corpus, reverse_sibling_order):
        block = recurse(
            working_bp,
            child,
            reverse_sibling_order=reverse_sibling_order,
            is_title_shown=is_title_shown,
            **kwargs,
        )
        if block:
            child_blocks.append(block)
    lines = _join_blocks(child_blocks)

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
