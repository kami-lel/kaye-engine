"""
render.tree.py

define ``render_blueprint_tree``
"""

import copy

from anytree import RenderTree

from .util import render_comment

__all__ = ("render_blueprint_tree",)


# constants  ####################################################################
CHECKMARKED_PREFIX = "[x] "
UNCHECKMARKED_PREFIX = "[ ] "
EMPTY_PREFIX = "    "


# auxiliaries  ###################################################################
def _create_pruned_tree_for_preview_recursively(blueprint, node):
    """
    create a `PromptCorpusNode` as root of a new **pruned** tree such that
    only nodes contained in `blueprint` is kept.
    This is done by traverse the tree and check if any nodes is contained
    in the blueprint

    (helper function used in ``render_blueprint_tree()``)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param node:
    :type node: BasePromptNode
    :return: root of the filtered node
    :rtype: PromptCorpusNode
    """
    new_node = copy.copy(node)  # an copy w/o children

    for child in node.children:
        if child in blueprint:
            new_child = _create_pruned_tree_for_preview_recursively(
                blueprint, child
            )
            new_child.parent = new_node

    return new_node


# Public API  ####################################################################
def render_blueprint_tree(
    blueprint,
    *,
    content_preview_lines=3,
    content_preview_width=64,
    show_full_tree=False,
    show_comment=False,
    display_name="",
):
    """
    generate **preview tree** of ``blueprint``,
    an human-readable representation


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param content_preview_lines: set maximum line count of
            *content preview* part, (excluding section heading line);
            defaults to 3
    :type content_preview_lines: int
    :param content_preview_width: set maximum column width of
            *content preview* part;
            defaults to 64.
    :type content_preview_width: int
    :param show_full_tree: whether to show the full corpus tree,
            regardless of node's inclusion in this blueprint;
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
    if show_full_tree:
        preview_tree = blueprint.corpus
    else:
        # create a duplicated tree,
        # but contains only nodes relevant to this blueprint
        preview_tree = _create_pruned_tree_for_preview_recursively(
            blueprint, blueprint.corpus
        )

    # generate content  --------------------------------------------------------
    lines = []
    for pre, fill, node in RenderTree(preview_tree):
        # line for tree structure
        checkmark_prefix = (
            CHECKMARKED_PREFIX
            if blueprint.is_checkmarked(hash(node))
            else UNCHECKMARKED_PREFIX
        )
        if node.is_root:
            checkmark_prefix = EMPTY_PREFIX

        # e.g. "[x] │   └── Style Guide Capitalization Style"
        node_line = checkmark_prefix + pre + node.name
        lines.append(node_line)

        # lines for content preview part
        if content_preview_lines:
            content_fill = EMPTY_PREFIX + fill
            lines.extend(
                (content_fill + line)[:content_preview_width]
                for line in node.content_lines()[:content_preview_lines]
            )

    # append comment line  -----------------------------------------------------
    if show_comment:
        comment_line = "<!-- " + render_comment(display_name) + " -->"
        lines.append(comment_line)

    return "\n".join(lines)
