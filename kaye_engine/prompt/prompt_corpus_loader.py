"""
prompt_corpus_loader.py

define ``load_corpus_tree``, ``get_corpus_tree`` and
``clear_corpus_tree`` -- the one parsed prompt corpus tree a process
holds

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
from .md_fence import compute_fenced_line_mask
from .prompt_corpus_node import PromptCorpusNode

__all__ = (
    "clear_corpus_tree",
    "get_corpus_tree",
    "load_corpus_tree",
)


# constants  ###################################################################
ROOT_NODE_NAME = "○"


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
    resolve one entry of ``load_corpus_tree``'s ``sources`` list --
    ``source`` a :class:`Path` is opened and read as a file; ``source``
    a ``str`` is used directly, as literal content


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


# the one parsed prompt corpus tree of this process
_corpus_tree = None


# Public API  ##################################################################


def load_corpus_tree(sources):  # ==============================================
    """
    concatenate ``sources``, in order, into one logical document, parse
    it into the process's **prompt corpus tree**, and hold it -- every
    dynamic node (each ``DYNAMIC_NODE_TYPES`` member, each
    ``ABBR_TAG_NODE_MEMBERS`` tag, and every registered glossary)
    auto-attaches unconditionally; an authored ``(name)`` heading, at
    any depth in ``sources``, fixes its preface and tree location in
    place of the heading -- else it falls back to a direct child of
    root

    Prerequisite: :func:`register_abbr_glossary` for every glossary
    named in a ``(name)`` heading of ``sources``


    :param sources: ordered sources to concatenate into one logical
            document -- each ``str`` entry is literal content, each
            ``Path`` entry is a markdown file to read
    :type sources: list[str or Path]
    :raises ValueError: a corpus tree is already loaded,
            ``sources`` contain a heading wrapped in
            parentheses -- reserved for dynamic nodes -- that resolves
            to no known dynamic node, or two headings resolve to the
            same dynamic node
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

    # read corpus content from sources, concatenated as if one file
    prompt_corpus_text = "\n\n".join(
        _read_content_source(source) for source in sources
    )

    # text split & clean up  ---------------------------------------------------
    # split to lines, then reduce 2+ empty lines into single empty line,
    # skipping lines inside a fenced code block
    text_lines = _collapse_unfenced_blank_runs(prompt_corpus_text.split("\n"))

    # create prompt corpus nodes  ----------------------------------------------
    tree = PromptCorpusNode.parse(ROOT_NODE_NAME, None, text_lines)

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
            "no corpus tree loaded; call load_corpus_tree(sources) first"
        )

    return _corpus_tree


def clear_corpus_tree():  # ====================================================
    """
    drop the loaded corpus tree so :func:`load_corpus_tree` may run
    again; a no-op when none is loaded
    """
    global _corpus_tree  # pylint: disable=global-statement

    _corpus_tree = None
