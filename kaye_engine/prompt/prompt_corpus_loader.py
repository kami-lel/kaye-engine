"""
prompt_corpus_loader.py

define ``register_corpus_under_node``, ``load_corpus_tree``,
``get_corpus_tree`` and ``clear_corpus_tree`` -- the one parsed prompt
corpus tree a process holds, built from the sources registered under
its nodes

Every dynamic node auto-attaches; an authored ``(name)`` heading, at
any depth, fixes its location and preface -- else it falls back to root.
"""

import functools
import re
from pathlib import Path

from anytree import PreOrderIter

from kaye_engine.abbr_collection import abbr_glossary_registry

from .dynamic_nodes import (
    ABBR_TAG_NODE_MEMBERS,
    DYNAMIC_NODE_TYPES,
    AbbrTagNode,
    GlossaryNode,
    resolve_dynamic_node_factory,
)
from .md_comment import strip_comment_blocks
from .md_fence import compute_fenced_line_mask
from .prompt_corpus_node import (
    HEADING_PREFIX_ELEMENT,
    PromptCorpusNode,
    split_sections,
)

__all__ = (
    "add_corpus_clear_hook",
    "clear_corpus_tree",
    "get_corpus_tree",
    "load_corpus_tree",
    "register_corpus_under_node",
)


# constants  ###################################################################
ROOT_NODE_NAME = "○"

_HEADING_PATTERN = re.compile(r"(#+) ")


# auxiliaries  #################################################################


def _is_parenthesized_heading(heading):
    """
    :return: whether ``heading`` uses the ``(...)`` syntax reserved for
            dynamic node headings
    :rtype: bool
    """
    return heading.startswith("(") and heading.endswith(")")


def _collapse_unfenced_blank_runs(text_lines):
    """
    reduce 3+ consecutive newlines to a single blank line within each
    maximal run of lines outside a fenced code block, leaving every
    line inside a fenced code block (blank or not) untouched -- each
    unfenced run is collapsed independently, via the same regex
    previously applied to the whole text, so unfenced behavior is
    unchanged and a fence boundary acts like a text boundary for its
    neighboring run

    (helper function used in ``load_corpus_tree()``)


    :param text_lines:
    :type text_lines: list[str]
    :return: ``text_lines`` with unfenced blank-line runs collapsed
    :rtype: list[str]
    """
    fenced_mask = compute_fenced_line_mask(text_lines)

    result = []
    segment_start = 0
    for idx in range(1, len(text_lines) + 1):
        at_end = idx == len(text_lines)
        if at_end or fenced_mask[idx] != fenced_mask[segment_start]:
            segment = text_lines[segment_start:idx]
            if fenced_mask[segment_start]:
                result.extend(segment)
            else:
                cleaned = re.sub(r"\n{3,}", "\n\n", "\n".join(segment))
                result.extend(cleaned.split("\n"))
            segment_start = idx

    return result


def _read_content_source(source):
    """
    resolve one registered source -- ``source`` a :class:`Path` is
    opened and read as a file; ``source`` a ``str`` is used directly, as
    literal content


    :param source: file to read, or literal content
    :type source: str or Path
    :return: the source's text content
    :rtype: str
    """
    if isinstance(source, Path):
        with open(source, "r", encoding="utf-8", newline="") as file:
            return file.read()

    return source


def _resolve_dynamic_heading(heading):
    """
    resolve a parenthesized ``heading`` via
    :func:`resolve_dynamic_node_factory` against the canonical kebab
    ``NAME`` universe -- returns ``(node_type, kwargs)`` where
    ``kwargs`` is the dict of parameters the match needs at
    construction time (empty for an engine-defined match), or
    ``(None, {})`` for an ordinary static heading
    """
    if not _is_parenthesized_heading(heading):
        return None, {}

    name = heading[1:-1]
    factory = resolve_dynamic_node_factory(name)

    if isinstance(factory, functools.partial):
        return factory.func, dict(factory.keywords)

    return factory, {}


def _normalize_node_path(node_path):
    """
    :return: ``node_path`` as a tuple of headings from the root
    :rtype: tuple[str, ...]
    :raises TypeError: ``node_path`` is neither a tuple nor a ``str``
    :raises ValueError: a heading is empty, a bare ``str`` looks like a
            file path, or a heading names a sidecar or dynamic node
    """
    if isinstance(node_path, str):
        if "/" in node_path or node_path.strip().endswith(".md"):
            raise ValueError(
                "node_path looks like a file path, not a heading: {!r}; "
                "pass (node_path, source) in that order".format(node_path)
            )
        node_path = (node_path,)

    if not isinstance(node_path, tuple):
        raise TypeError(
            "node_path must be a tuple of headings or a str, got {}".format(
                type(node_path).__name__
            )
        )

    for heading in node_path:
        if not isinstance(heading, str) or not heading.strip():
            raise ValueError(
                "node_path heading must be a non-empty str: {!r}".format(
                    node_path
                )
            )
        if heading.startswith("{") or _is_parenthesized_heading(heading):
            raise ValueError(
                "cannot register corpus under a sidecar or dynamic node: "
                "{!r}".format(node_path)
            )

    return node_path


def _check_source(source):
    """
    :raises TypeError: ``source`` is neither a ``Path`` nor a ``str``
    :raises ValueError: a ``str`` source looks like a file name
    """
    if isinstance(source, Path):
        return
    if not isinstance(source, str):
        raise TypeError(
            "source must be a Path or a str, got {}".format(
                type(source).__name__
            )
        )
    if source.strip().endswith(".md"):
        raise ValueError(
            "str source ending in .md is read as literal content; "
            "pass a Path to read a file: {!r}".format(source)
        )


def _describe_source(source, idx):
    if isinstance(source, Path):
        return str(source)
    return "literal source #{}".format(idx)


def _read_source_lines(source):
    """
    :return: ``source``'s lines, markdown comment blocks dropped and
            unfenced blank runs collapsed, on its own so no fence or
            comment leaks into another source
    :rtype: list[str]
    """
    return _collapse_unfenced_blank_runs(
        strip_comment_blocks(_read_content_source(source).split("\n"))
    )


def _check_heading_level(text_lines, depth, label):
    """
    :raises ValueError: a heading of ``text_lines`` sits shallower or,
            at the top, deeper than one level below a node at ``depth``
    """
    fenced_mask = compute_fenced_line_mask(text_lines)
    levels = [
        len(match.group(1))
        for idx, line in enumerate(text_lines)
        if not fenced_mask[idx]
        and (match := _HEADING_PATTERN.match(line)) is not None
    ]
    if levels and min(levels) != depth + 1:
        raise ValueError(
            "{}: top headings must be {!r}, one level below the target, "
            "found {!r}".format(
                label,
                HEADING_PREFIX_ELEMENT * (depth + 1),
                HEADING_PREFIX_ELEMENT * min(levels),
            )
        )


def _find_node(tree, node_path):
    """
    :return: the node at ``node_path`` under ``tree``, or ``None``
    """
    node = tree
    for heading in node_path:
        node = next(
            (child for child in node.children if child.name == heading),
            None,
        )
        if node is None:
            return None
    return node


def _check_unique_siblings(node, owner_by_node, label):
    """
    :raises ValueError: 2 children of ``node`` or of any descendant share
            a heading
    """
    seen = {}
    for child in node.children:
        if child.name in seen:
            raise ValueError(
                "duplicate heading {!r} under {!r}: from {} and {}".format(
                    child.name,
                    "/".join(node.generate_lineage()) or ROOT_NODE_NAME,
                    owner_by_node.get(id(seen[child.name]), label),
                    owner_by_node.get(id(child), label),
                )
            )
        seen[child.name] = child
        _check_unique_siblings(child, owner_by_node, label)


def _graft(target, source_lines, label, owner_by_node):
    """
    parse ``source_lines`` as children of ``target``, appending any
    leading content before the first heading to ``target``'s own content
    """
    _check_heading_level(source_lines, target.depth, label)

    leading_lines, child_specs = split_sections(source_lines, target.depth)
    if any(line.strip() for line in leading_lines):
        target._content_lines = [  # pylint: disable=protected-access
            *target.content_lines(),
            *leading_lines,
        ]

    for heading, child_lines in child_specs:
        child = PromptCorpusNode.parse(heading, target, child_lines)
        for node in PreOrderIter(child):
            owner_by_node[id(node)] = label

    _check_unique_siblings(target, owner_by_node, label)


def _build_static_tree(registrations):
    """
    graft every registration, in passes: each pass grafts, in
    registration order, every registration whose target exists, until
    none is left


    :raises ValueError: a target that never appears, or any error of
            :func:`_graft`
    :return: the root of the static tree, before dynamic nodes attach
    :rtype: PromptCorpusNode
    """
    tree = PromptCorpusNode(ROOT_NODE_NAME, None, [])
    owner_by_node = {}

    pending = [
        (node_path, source, _describe_source(source, idx))
        for idx, (node_path, source) in enumerate(registrations)
    ]
    while pending:
        left = []
        for node_path, source, label in pending:
            target = _find_node(tree, node_path)
            if target is None:
                left.append((node_path, source, label))
                continue
            _graft(
                target, _read_source_lines(source), label, owner_by_node
            )

        if len(left) == len(pending):
            raise ValueError(
                "no corpus node at path {} for {}".format(
                    ", ".join(repr(list(p)) for p, _, _ in left),
                    ", ".join(label for _, _, label in left),
                )
            )
        pending = left

    return tree


# the one parsed prompt corpus tree of this process
_corpus_tree = None

# (node path, source) pairs the tree is built from, in registration order
_corpus_registrations = []

# callbacks run by clear_corpus_tree(), dropping data derived from the tree
_clear_hooks = []


# Public API  ##################################################################


def register_corpus_under_node(node_path, source):  # =========================
    """
    record ``source`` to be parsed under the node at ``node_path`` when
    :func:`load_corpus_tree` builds the tree; nothing is read or parsed
    now

    ``source``'s top headings must sit exactly one level below the
    target: ``#`` under the root, ``###`` under a ``## a`` node; any
    content before its first heading is appended to the target's own
    content


    :param node_path: headings from the root to the target node; ``()``
            is the root; a bare ``str`` without ``/`` or ``.md`` is a
            one-heading path
    :type node_path: tuple[str, ...] or str
    :param source: markdown file to read, or literal content
    :type source: Path or str
    :raises TypeError: ``node_path`` or ``source`` has the wrong type
    :raises ValueError: a corpus tree is already loaded, ``node_path``
            names a sidecar or dynamic node or looks like a file path,
            or a ``str`` ``source`` ends in ``.md``
    """
    if _corpus_tree is not None:
        raise ValueError(
            "a corpus tree is already loaded; register corpus before "
            "load_corpus_tree(), or call clear_corpus_tree() first"
        )

    node_path = _normalize_node_path(node_path)
    _check_source(source)
    _corpus_registrations.append((node_path, source))


def load_corpus_tree():  # =====================================================
    """
    parse every source registered via :func:`register_corpus_under_node`
    on its own and graft it under its target node, building the
    process's **prompt corpus tree**, and hold it -- every dynamic node
    (each ``DYNAMIC_NODE_TYPES`` member, each ``ABBR_TAG_NODE_MEMBERS``
    tag, and every registered glossary) auto-attaches unconditionally;
    an authored ``(name)`` heading, at any depth of any source, fixes its
    preface and tree location in place of the heading -- else it falls
    back to a direct child of root

    registrations graft in passes, so they may come in any order; only
    sibling order under one node follows registration order

    a line-anchored markdown comment (``<!-- ... -->``) outside a fenced
    code block or tag block is dropped on load, per source, so it never
    renders and never reaches another source

    Prerequisite: :func:`register_abbr_glossary` for every glossary
    named in a ``(name)`` heading of a source


    :raises ValueError: a corpus tree is already loaded, a registered
            target never appears, a source's top headings sit at the
            wrong level, 2 siblings share a heading, a heading wrapped in
            parentheses -- reserved for dynamic nodes -- resolves to no
            known dynamic node, or two headings resolve to the same
            dynamic node
    :raises FileNotFoundError:
    :raises IOError:
    :return: **root** node of the parsed *prompt corpus tree*
    :rtype: PromptCorpusNode
    """
    global _corpus_tree  # pylint: disable=global-statement

    if _corpus_tree is not None:
        raise ValueError(
            "a corpus tree is already loaded; call clear_corpus_tree() first"
        )

    tree = _build_static_tree(_corpus_registrations)

    # add dynamic nodes  -------------------------------------------------------
    # locate every "(name)" heading that resolves to a dynamic node;
    # unresolved headings raise inside _resolve_dynamic_heading
    locations = {}
    for node in PreOrderIter(tree):
        if node is tree:
            continue

        node_type, kwargs = _resolve_dynamic_heading(node.name)
        if node_type is None:
            continue

        key = (node_type, tuple(sorted(kwargs.items())))
        if key in locations:
            raise ValueError(
                "duplicate heading for dynamic node: {}".format(node.name)
            )
        locations[key] = node

    def _attach(new_node, key):
        # swap into the heading's position, or fall back to root
        heading_node = locations.get(key)
        if heading_node is None:
            new_node.parent = tree
            return

        parent = heading_node.parent
        parent.children = tuple(
            new_node if child is heading_node else child
            for child in parent.children
        )

    def _preface_for(key):
        heading_node = locations.get(key)
        if heading_node is None:
            return ()
        return tuple(heading_node.content_lines())

    for node_type in DYNAMIC_NODE_TYPES:
        key = (node_type, ())
        _attach(node_type(None, preface=_preface_for(key)), key)

    for abbr_tag in ABBR_TAG_NODE_MEMBERS:
        key = (AbbrTagNode, (("abbr_tag", abbr_tag),))
        _attach(
            AbbrTagNode(None, abbr_tag=abbr_tag, preface=_preface_for(key)), key
        )

    for glossary_name in sorted(abbr_glossary_registry):
        key = (GlossaryNode, (("glossary_name", glossary_name),))
        _attach(
            GlossaryNode(
                None, glossary_name=glossary_name, preface=_preface_for(key)
            ),
            key,
        )

    _corpus_tree = tree

    return tree


def get_corpus_tree():  # ======================================================
    """
    Prerequisite: :func:`load_corpus_tree` called


    :raises ValueError: no corpus tree is loaded yet
    :return: **root** node of the loaded *prompt corpus tree*
    :rtype: PromptCorpusNode
    """
    if _corpus_tree is None:
        raise ValueError(
            "no corpus tree loaded; call load_corpus_tree() first"
        )

    return _corpus_tree


def clear_corpus_tree():  # ====================================================
    """
    drop the loaded corpus tree and every corpus registration, so
    sources may be registered and :func:`load_corpus_tree` run again; a
    no-op when none is loaded
    """
    global _corpus_tree  # pylint: disable=global-statement

    _corpus_tree = None
    _corpus_registrations.clear()
    for hook in _clear_hooks:
        hook()


def add_corpus_clear_hook(hook):  # ============================================
    """
    register ``hook`` to run on every :func:`clear_corpus_tree`, so data
    derived from the tree is dropped together with it


    :param hook: zero-argument callable
    :type hook: Callable[[], None]
    """
    if hook not in _clear_hooks:
        _clear_hooks.append(hook)
