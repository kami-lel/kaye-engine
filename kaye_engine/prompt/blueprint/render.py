"""
render.py

define:

- ``render_blueprint_tree``
- ``render_prompt_lines``
- ``render_comment``
- ``REPLACEMENT_NEWLINE_SYMBOL``
"""

import copy
import importlib.metadata
from datetime import datetime

from anytree import RenderTree, PreOrderIter

from kaye_engine import PACKAGE_NAME
from ..prompt_corpus_node import HEADING_PREFIX_ELEMENT
from ..sidecar_node import get_sidecar_name

__all__ = (
    "render_blueprint_tree",
    "render_prompt_lines",
    "render_comment",
    "REPLACEMENT_NEWLINE_SYMBOL",
)


# constants  ###################################################################
CHECKMARKED_PREFIX = "[x] "
UNCHECKMARKED_PREFIX = "[ ] "
EMPTY_PREFIX = "    "
REPLACEMENT_NEWLINE_SYMBOL = "↵"
NO_TRIM_SPARSENESS = 99


# auxiliaries  #################################################################
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


def _build_affordance_sidecar_map(affordances):
    """
    build a sidecar-name -> should-checkmark lookup from every entry in
    ``affordance_registry``, given which affordances are available

    (helper function used in ``_splice_conditional_sidecars()``)


    :param affordances: canonical names of affordances available on the
            target surface
    :type affordances: collections.abc.Iterable[str]
    :return: sidecar name -> whether it should be auto-checkmarked
    :rtype: dict[str, bool]
    """
    from ..affordance_registry import affordance_registry

    available = set(affordances)
    sidecar_map = {}
    for entry in affordance_registry.values():
        is_available = entry.canonical_name in available
        sidecar_map[entry.usage_sidecar_name] = is_available
        sidecar_map[entry.lack_sidecar_name] = not is_available
    return sidecar_map


def _splice_conditional_sidecars(blueprint, *, contains_sidecars, affordances):
    """
    auto-checkmark conditional sidecar nodes ahead of rendering -- both
    plain ``contains_sidecars`` name matches and, when ``affordances``
    is given, the ``Usage``/``Lack`` sidecar pair for every entry in
    ``affordance_registry``

    (helper function used in ``render_prompt_lines()``)


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param contains_sidecars: see ``render_prompt_lines()``
    :type contains_sidecars: collections.abc.Iterable[str]
    :param affordances: see ``render_prompt_lines()``
    :type affordances: collections.abc.Iterable[str] or None
    :return: ``blueprint``, or a checkmark-spliced copy of it when either
            mechanism has anything to apply
    :rtype: PromptBlueprint
    """
    affordance_sidecar_names = (
        _build_affordance_sidecar_map(affordances)
        if affordances is not None
        else None
    )

    if not contains_sidecars and affordance_sidecar_names is None:
        return blueprint

    working_bp = copy.copy(blueprint)
    for node in PreOrderIter(working_bp.corpus):
        sidecar_name = get_sidecar_name(node)
        if sidecar_name is None or not working_bp.is_checkmarked(node.parent):
            continue
        if sidecar_name in contains_sidecars or (
            affordance_sidecar_names is not None
            and affordance_sidecar_names.get(sidecar_name)
        ):
            working_bp.checkmark(node)

    return working_bp


def _apply_sparseness(lines, sparseness):
    """
    apply the ``sparseness`` blank-line policy to a list of prompt lines

    (helper function used in ``render_prompt_lines()``)


    :param lines:
    :type lines: list[str]
    :param sparseness: see ``render_prompt_lines()`` for the full contract
    :type sparseness: int
    :return: lines with the ``sparseness`` policy applied
    :rtype: list[str]
    """
    if sparseness == NO_TRIM_SPARSENESS:
        return lines

    # trim leading/trailing empty lines unconditionally
    start, end = 0, len(lines)
    while start < end and lines[start] == "":
        start += 1
    while end > start and lines[end - 1] == "":
        end -= 1
    trimmed = lines[start:end]

    if sparseness == -1:
        return [REPLACEMENT_NEWLINE_SYMBOL.join(trimmed)]

    result = []
    empty_run = 0
    for line in trimmed:
        if line == "":
            empty_run += 1
            continue
        result.extend([""] * min(empty_run, sparseness))
        empty_run = 0
        result.append(line)
    result.extend([""] * min(empty_run, sparseness))

    return result


# Public API  ##################################################################


def render_blueprint_tree(  # ==================================================
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


def render_prompt_lines(  # ====================================================
    blueprint,
    *,
    show_comment=False,
    disable_first_heading=False,
    contains_sidecars=(),
    affordances=None,
    display_name="",
    sparseness=1,
    **kwargs,
):
    """
    generate prompt as a list of lines from ``blueprint``

    optionally auto-checkmarks sidecar nodes of specified name(s) before
    rendering.


    :param blueprint:
    :type blueprint: PromptBlueprint
    :param show_comment: show comment part after last line;
            defaults to False
    :type show_comment: bool, optional
    :param disable_first_heading: whether disable showing top heading;
            defaults to False
    :type disable_first_heading: bool, optional
    :param contains_sidecars: auto-checkmark conditional sidecar nodes
            whose name is in this collection and whose parent is
            checkmarked (e.g., ``("Claude Tool:TodoWrite",)``);
            defaults to ``()`` (disabled)
    :type contains_sidecars: Iterable[str], optional
    :param affordances: per ``affordance_registry`` entry,
            checkmarks ``Usage`` node if entry's ``canonical_name`` in
            this collection, else ``Lack`` node; either way, only if
            parent already checkmarked.
            ``None``: pass off (default).
            ``()``: pass on, every affordance unavailable.
    :type affordances: Iterable[str] or None, optional
    :param display_name: blueprint's human-readable name, included in the
            comment when ``show_comment`` is set; defaults to ""
    :type display_name: str, optional
    :param sparseness: controls how runs of blank lines collapse:

    - ``-1`` collapses the whole output into a single line, joined with
            ``REPLACEMENT_NEWLINE_SYMBOL`` in place of every newline
    - ``0`` removes all blank lines
    - ``1`` collapses every run of blank lines to a single blank line (default)
    - ``2`` caps runs at two blank lines, and so on
    - 〃
    - ``99`` disables trimming entirely

    :type sparseness: int, optional
    :return: list of prompt lines
    :rtype: list[str]
    """
    working_bp = _splice_conditional_sidecars(
        blueprint, contains_sidecars=contains_sidecars, affordances=affordances
    )

    lines = []

    should_skip_heading = disable_first_heading

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

    if show_comment:
        lines.append("<!-- " + render_comment(display_name) + " -->")

    return _apply_sparseness(lines, sparseness)


def render_comment(display_name=""):  # ========================================
    """
    :param display_name: blueprint's human-readable name, omitted from the
            comment when empty; defaults to ""
    :type display_name: str, optional
    :return: prompt comment containing blueprint name and Kaye Engine version
    :rtype: str

    :example:
    >>> print(render_comment("Chat"))
    'blueprint: Chat; Kaye Engine v1.2.3'
    """
    kaye_version = importlib.metadata.version(PACKAGE_NAME)

    # append render date-time in version for alpha releases
    if "a" in kaye_version:
        kaye_version += datetime.now().strftime(".0%Y%m%d%H%M%S")

    name_part = "blueprint: {}; ".format(display_name) if display_name else ""

    return "{}Kaye Engine v{}".format(name_part, kaye_version)
