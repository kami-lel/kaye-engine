"""
prompt_corpus_loader.py

define ``load_corpus_tree`` and ``get_corpus_tree`` -- a name-keyed
cache of parsed prompt corpus trees -- plus ``get_default_corpus_tree``,
resolving whichever tree was loaded with ``is_default_tree=True``
"""

import re

from anytree import PreOrderIter

from kaye_engine.abbr_collection import abbr_glossary_registry

from .dynamic_nodes import (
    ABBR_TAG_NODE_MEMBERS,
    DYNAMIC_NODE_TYPES,
    AbbrTagNode,
    GlossaryNode,
    heading_for_abbr_tag,
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
    resolve a parenthesized ``heading`` against ``DYNAMIC_NODE_TYPES``
    first, then ``ABBR_TAG_NODE_MEMBERS``, then against every glossary
    name known to ``abbr_glossary_registry`` -- returns
    ``(node_type, kwargs)`` where ``kwargs`` is the dict of parameters
    the match needs at construction time (empty for an engine-defined
    match), or ``(None, {})`` for an ordinary static heading
    """
    if not _is_parenthesized_heading(heading):
        return None, {}

    for node_type in DYNAMIC_NODE_TYPES:
        if heading == "(" + node_type.HEADING + ")":
            return node_type, {}

    inner = heading[1:-1]

    for abbr_tag in ABBR_TAG_NODE_MEMBERS:
        if inner == heading_for_abbr_tag(abbr_tag):
            return AbbrTagNode, {"abbr_tag": abbr_tag}

    if inner in abbr_glossary_registry:
        return GlossaryNode, {"glossary_name": inner}

    raise ValueError("unrecognized dynamic node heading: {}".format(heading))


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
    ``tree_name``, attaching the various dynamic nodes once


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
            exists, or ``file_path`` contains a heading wrapped in
            parentheses -- reserved for dynamic nodes, and only valid
            as a direct child of the root
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
    prefaces = {}
    abbr_tag_prefaces = {}
    glossary_prefaces = {}
    for child in list(tree.children):
        node_type, kwargs = _resolve_dynamic_heading(child.name)
        if node_type is AbbrTagNode:
            abbr_tag_prefaces[kwargs["abbr_tag"]] = tuple(child.content_lines())
            child.parent = None
        elif node_type is GlossaryNode:
            glossary_prefaces[kwargs["glossary_name"]] = tuple(
                child.content_lines()
            )
            child.parent = None
        elif node_type is not None:
            prefaces[node_type] = tuple(child.content_lines())
            child.parent = None

    # any remaining "(...)" heading is invalid -- that syntax is reserved
    # for dynamic nodes, which attach only as direct children of the root
    for node in PreOrderIter(tree):
        if node is not tree and _is_parenthesized_heading(node.name):
            raise ValueError(
                "dynamic node heading only allowed as a direct child "
                "of root: {}".format(node.name)
            )

    for node_type in DYNAMIC_NODE_TYPES:
        node_type(tree, preface=prefaces.get(node_type, ()))

    for abbr_tag in ABBR_TAG_NODE_MEMBERS:
        AbbrTagNode(
            tree, abbr_tag=abbr_tag, preface=abbr_tag_prefaces.get(abbr_tag, ())
        )

    for glossary_name, preface in glossary_prefaces.items():
        GlossaryNode(tree, glossary_name=glossary_name, preface=preface)

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
    :raises ValueError: no tree has been flagged default yet, via
            ``load_corpus_tree(..., is_default_tree=True)``
    :return: **root** node of the corpus tree flagged default
    :rtype: PromptCorpusNode
    """
    if _default_tree_name is None:
        raise ValueError(
            "no default corpus tree set; call "
            "load_corpus_tree(..., is_default_tree=True) first"
        )

    return get_corpus_tree(_default_tree_name)
