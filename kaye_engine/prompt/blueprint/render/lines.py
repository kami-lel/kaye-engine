"""
render.lines.py

define:

- ``render_prompt_lines``
- ``render_negative_prompt_lines``
"""

from anytree import PreOrderIter

from ...prompt_corpus_node import HEADING_PREFIX_ELEMENT
from ...sidecar_node import AVOID_NAME, get_sidecar_name
from ..render_mode import RenderMode
from ..render_profile import RenderProfile
from .sidecar_splice import _splice_conditional_sidecars
from .util import apply_sparseness, render_comment

__all__ = (
    "render_negative_prompt_lines",
    "render_prompt_lines",
)


def _render_negative_prompt_node_recursively(blueprint, node, **kwargs):
    """
    recursively render one checkmarked node's contribution to a
    negative prompt

    a node contributes only when it, or one of its descendants,
    carries an ``{avoid}`` sidecar child: its own heading is printed
    (the ``{avoid}`` child's heading never is), followed by that
    child's content, then any contributing descendants in the same
    fashion; a node with neither is omitted entirely, and non-``avoid``
    sidecar children (``{description}``, ``{when_to_use}``, ...) never
    contribute

    (helper function used in ``render_negative_prompt_lines()``)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param node: node to render, never the corpus root
    :type node: BasePromptNode
    :param kwargs: further render options forwarded to the ``{avoid}``
            node's ``content_lines(**kwargs)``
    :return: rendered lines for ``node`` and its descendants, or an
            empty list when nothing in this subtree contributes
    :rtype: list[str]
    """
    if not blueprint.is_checkmarked(node):
        return []

    own_avoid_lines = []
    child_blocks = []

    for child in node.children:
        sidecar_name = get_sidecar_name(child)
        if sidecar_name == AVOID_NAME:
            own_avoid_lines = child.content_lines(**kwargs)
        elif sidecar_name is None:
            block = _render_negative_prompt_node_recursively(
                blueprint, child, **kwargs
            )
            if block:
                child_blocks.append(block)

    if not own_avoid_lines and not child_blocks:
        return []

    lines = [HEADING_PREFIX_ELEMENT * node.depth + " " + node.name]
    lines.extend(own_avoid_lines)

    for block in child_blocks:
        if len(lines) > 1:
            lines.append("")
        lines.extend(block)

    return lines


def _render_prompt_node_post_order_recursively(blueprint, node, **kwargs):
    """
    recursively render one node's contribution for
    ``RenderMode.POST_ORDER``: every child's full subtree first (each
    following the same rule, siblings kept in original relative
    order), then this node's own heading and content last, only when
    this node itself is checkmarked -- checkmarking is evaluated
    per-node, independent of any ancestor's, matching the flat
    ``PreOrderIter`` walk this replaces

    (helper function used in ``render_prompt_lines()`` when
    ``RenderMode.POST_ORDER`` is set)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param node:
    :type node: BasePromptNode
    :param kwargs: further render options forwarded to each
            checkmarked node's ``content_lines(**kwargs)``
    :return: rendered lines for ``node`` and its descendants, or an
            empty list when nothing in this subtree contributes
    :rtype: list[str]
    """
    child_blocks = []
    for child in node.children:
        block = _render_prompt_node_post_order_recursively(
            blueprint, child, **kwargs
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

    lines = []
    for block in child_blocks:
        if lines:
            lines.append("")
        lines.extend(block)

    if own_lines:
        if lines:
            lines.append("")
        lines.extend(own_lines)

    return lines


def _render_negative_prompt_node_post_order_recursively(
    blueprint, node, **kwargs
):
    """
    (``RenderMode.POST_ORDER`` counterpart of
    ``_render_negative_prompt_node_recursively``) recursively render
    one checkmarked node's contribution to a negative prompt, with
    every contributing child's block first (children kept in original
    relative order), then this node's own heading and ``{avoid}``
    content last

    (helper function used in ``render_negative_prompt_lines()`` when
    ``RenderMode.POST_ORDER`` is set)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param node: node to render, never the corpus root
    :type node: BasePromptNode
    :param kwargs: further render options forwarded to the ``{avoid}``
            node's ``content_lines(**kwargs)``
    :return: rendered lines for ``node`` and its descendants, or an
            empty list when nothing in this subtree contributes
    :rtype: list[str]
    """
    if not blueprint.is_checkmarked(node):
        return []

    own_avoid_lines = []
    child_blocks = []

    for child in node.children:
        sidecar_name = get_sidecar_name(child)
        if sidecar_name == AVOID_NAME:
            own_avoid_lines = child.content_lines(**kwargs)
        elif sidecar_name is None:
            block = _render_negative_prompt_node_post_order_recursively(
                blueprint, child, **kwargs
            )
            if block:
                child_blocks.append(block)

    if not own_avoid_lines and not child_blocks:
        return []

    lines = []
    for block in child_blocks:
        if lines:
            lines.append("")
        lines.extend(block)

    own_lines = [HEADING_PREFIX_ELEMENT * node.depth + " " + node.name]
    own_lines.extend(own_avoid_lines)

    if lines:
        lines.append("")
    lines.extend(own_lines)

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


def render_prompt_lines(
    blueprint,
    *,
    profile=RenderProfile(),
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
            ``variants``, ``display_name``, ``sparseness``, plus the
            glossary-related fields); defaults to a plain
            `RenderProfile()`
    :type profile: RenderProfile, optional
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

    if RenderMode.POST_ORDER in profile.mode:
        lines = _render_prompt_node_post_order_recursively(
            working_bp, working_bp.corpus, **kwargs
        )
        if profile.disable_first_heading:
            lines = _remove_first_heading_line(lines)
    else:
        lines = []

        should_skip_heading = profile.disable_first_heading

        last_node_idx = working_bp.corpus.size - 1
        for i, node in enumerate(PreOrderIter(working_bp.corpus)):
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

    if profile.show_comment:
        lines.append("<!-- " + render_comment(profile.display_name) + " -->")

    if RenderMode._IMAGE in profile.mode:
        lines = _flatten_headings_for_image_mode(lines)

    return apply_sparseness(lines, profile.sparseness)


def render_negative_prompt_lines(
    blueprint,
    *,
    profile=RenderProfile(),
    **kwargs,
):
    """
    generate **negative prompt** as a list of lines from ``blueprint``

    walks every checkmarked node in ``blueprint``; a node's own
    ``{avoid}`` sidecar child supplies its printed content (that
    child's own heading is never shown), and a node is printed at all
    only when it or some descendant carries ``{avoid}`` content --
    branches with none are omitted entirely


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param profile: bundled render settings -- of `RenderProfile`'s
            fields, only ``conditional_sidecars``, ``variants``,
            ``show_comment``, ``display_name``, and ``sparseness``
            apply here; defaults to a plain `RenderProfile()`
    :type profile: RenderProfile, optional
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

    recurse = (
        _render_negative_prompt_node_post_order_recursively
        if RenderMode.POST_ORDER in profile.mode
        else _render_negative_prompt_node_recursively
    )

    lines = []
    for child in working_bp.corpus.children:
        block = recurse(working_bp, child, **kwargs)
        if not block:
            continue
        if lines:
            lines.append("")
        lines.extend(block)

    if profile.show_comment:
        lines.append("<!-- " + render_comment(profile.display_name) + " -->")

    if RenderMode._IMAGE in profile.mode:
        lines = _flatten_headings_for_image_mode(lines)

    return apply_sparseness(lines, profile.sparseness)
