"""
render.tree.py

define ``render_blueprint_tree``
"""

from .comment import render_comment_lines

__all__ = ("render_blueprint_tree",)


# constants  ####################################################################
CHECKMARKED_PREFIX = "[x] "
UNCHECKMARKED_PREFIX = "[ ] "
EMPTY_PREFIX = "    "

# branch drawing, as ``anytree``'s ``ContStyle`` draws it
_BRANCH_MID = "├── "
_BRANCH_END = "└── "
_BRANCH_VERTICAL = "│   "
_BRANCH_BLANK = "    "


# auxiliaries  ###################################################################
def _compute_visible_mask(selection):
    """
    :return: mask of every selected node plus all its ancestors, root
            included
    :rtype: int
    """
    index = selection.index

    visible = 1  # root
    mask = selection.mask
    while mask:
        low = mask & -mask
        mask ^= low
        idx = low.bit_length() - 1
        while idx >= 0 and not visible >> idx & 1:
            visible |= 1 << idx
            idx = index.parent_idxs[idx]

    return visible


def _content_preview_lines(index, idx):
    block = index.blocks[idx]
    if block is not None:
        return block[1:]
    return index.node_objs[idx].content_lines()


# Public API  ####################################################################
def render_blueprint_tree(
    selection,
    *,
    content_preview_lines=3,
    content_preview_width=64,
    show_full_tree=False,
    show_comment=False,
    display_name="",
):
    """
    generate **preview tree** of ``selection``,
    an human-readable representation -- every selected node, with its
    ancestors so the structure stays readable


    :param selection: nodes to show as checkmarked
    :type selection: BlueprintSelection
    :param content_preview_lines: set maximum line count of
            *content preview* part, (excluding section heading line);
            defaults to 3
    :type content_preview_lines: int
    :param content_preview_width: set maximum column width of
            *content preview* part;
            defaults to 64.
    :type content_preview_width: int
    :param show_full_tree: whether to show the full corpus tree,
            regardless of node's selection;
    :type show_full_tree: bool, optional
    :param show_comment: show comment part after last line;
            defaults to False
    :type show_comment: bool, optional
    :param display_name: blueprint's human-readable name, included in the
            comment when ``show_comment`` is set; defaults to ""
    :type display_name: str, optional
    :return: the preview tree
    :rtype: str
    """
    index = selection.index
    visible = (
        (1 << len(index.node_objs)) - 1
        if show_full_tree
        else _compute_visible_mask(selection)
    )

    lines = []

    def _walk(idx, pre, fill):
        if idx == 0:
            checkmark_prefix = EMPTY_PREFIX
        elif selection.mask >> idx & 1:
            checkmark_prefix = CHECKMARKED_PREFIX
        else:
            checkmark_prefix = UNCHECKMARKED_PREFIX

        # e.g. "[x] │   └── Style Guide Capitalization Style"
        lines.append(checkmark_prefix + pre + index.node_objs[idx].name)

        # lines for content preview part
        if content_preview_lines:
            content_fill = EMPTY_PREFIX + fill
            lines.extend(
                (content_fill + line)[:content_preview_width]
                for line in _content_preview_lines(index, idx)[
                    :content_preview_lines
                ]
            )

        children = [c for c in index.child_idxs[idx] if visible >> c & 1]
        for position, child_idx in enumerate(children):
            if position == len(children) - 1:
                _walk(child_idx, fill + _BRANCH_END, fill + _BRANCH_BLANK)
            else:
                _walk(child_idx, fill + _BRANCH_MID, fill + _BRANCH_VERTICAL)

    _walk(0, "", "")

    # append comment line  -----------------------------------------------------
    if show_comment:
        lines.extend(render_comment_lines(display_name))

    return "\n".join(lines)
