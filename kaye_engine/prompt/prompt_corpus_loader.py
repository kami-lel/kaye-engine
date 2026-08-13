"""
prompt_corpus_loader.py

define ``load_corpus_tree`` and ``get_corpus_tree`` -- a name-keyed
cache of parsed prompt corpus trees -- plus ``get_default_corpus_tree``,
resolving whichever tree was loaded with ``is_default_tree=True``

Every dynamic node auto-attaches; an authored ``(name)`` heading, at
any depth, fixes its location and preface -- else it falls back to root.
"""

import functools
import re

from anytree import PreOrderIter

from kaye_engine.abbr_collection import abbr_glossary_registry

from .dynamic_nodes import (
    ABBR_TAG_NODE_MEMBERS,
    DYNAMIC_NODE_TYPES,
    AbbrTagNode,
    GlossaryNode,
    resolve_dynamic_node_factory,
)
from .prompt_corpus_node import PromptCorpusNode

__all__ = (
    "get_corpus_tree",
    "get_default_corpus_tree",
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


# name-keyed cache of parsed prompt corpus trees
_corpus_tree_cache = {}

# name of the tree flagged as default via load_corpus_tree(is_default_tree=True)
_default_tree_name = None


# Public API  ##################################################################


def load_corpus_tree(  # =======================================================
    tree_name, file_path, *, is_default_tree=False
):
    """
    parse ``file_path`` into a **prompt corpus tree** and cache it under
    ``tree_name`` -- every dynamic node (each ``DYNAMIC_NODE_TYPES``
    member, each ``ABBR_TAG_NODE_MEMBERS`` tag, and every registered
    glossary) auto-attaches unconditionally; an authored ``(name)``
    heading, at any depth in ``file_path``, fixes its preface and tree
    location in place of the heading -- else it falls back to a direct
    child of root

    Prerequisite: :func:`register_abbr_glossary` for every glossary
    named in a ``(name)`` heading of ``file_path``


    :param tree_name: key this tree is cached under; every subsequent
            :func:`get_corpus_tree` call with this name returns the
            same tree object
    :type tree_name: str
    :param file_path: path of the markdown file to parse
    :type file_path: Path or str
    :param is_default_tree: flag this tree as the **default** corpus
            tree, retrievable via :func:`get_default_corpus_tree`
            without knowing ``tree_name``; only one tree may ever be
            flagged default per process
    :type is_default_tree: bool, optional
    :raises ValueError: ``tree_name`` is already registered,
            ``is_default_tree`` is set while a default tree already
            exists, ``file_path`` contains a heading wrapped in
            parentheses -- reserved for dynamic nodes -- that resolves
            to no known dynamic node, or two headings resolve to the
            same dynamic node
    :raises FileNotFoundError:
    :raises IOError:
    :return: **root** node of the parsed *prompt corpus tree*
    :rtype: PromptCorpusNode
    """
    global _default_tree_name  # pylint: disable=global-statement

    if tree_name in _corpus_tree_cache:
        raise ValueError("duplicate corpus tree name: {}".format(tree_name))

    if is_default_tree and _default_tree_name is not None:
        raise ValueError(
            "a default corpus tree is already set: {}".format(
                _default_tree_name
            )
        )

    # read corpus content from file
    with open(file_path, "r", encoding="utf-8", newline="") as file:
        prompt_corpus_text = file.read()

    # text split & clean up  ---------------------------------------------------
    # reduce 2+ empty lines into single empty line
    text_cleanup = re.sub(r"\n{3,}", "\n\n", prompt_corpus_text)
    # split to lines
    text_lines = list(text_cleanup.split("\n"))

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

    _corpus_tree_cache[tree_name] = tree

    if is_default_tree:
        _default_tree_name = tree_name

    return tree


def get_corpus_tree(tree_name):  # =============================================
    """
    :param tree_name: key a tree was previously cached under via
            :func:`load_corpus_tree`
    :type tree_name: str
    :raises KeyError: no tree is registered under ``tree_name``
    :return: **root** node of the cached *prompt corpus tree*
    :rtype: PromptCorpusNode
    """
    try:
        return _corpus_tree_cache[tree_name]
    except KeyError as err:
        raise KeyError(
            "no corpus tree registered under name: {}".format(tree_name)
        ) from err


def get_default_corpus_tree():  # ==============================================
    """
    Prerequisite: :func:`load_corpus_tree` called with
    ``is_default_tree=True``


    :raises ValueError: no tree has been flagged default yet
    :return: **root** node of the corpus tree flagged default
    :rtype: PromptCorpusNode
    """
    if _default_tree_name is None:
        raise ValueError(
            "no default corpus tree set; call "
            "load_corpus_tree(..., is_default_tree=True) first"
        )

    return get_corpus_tree(_default_tree_name)
