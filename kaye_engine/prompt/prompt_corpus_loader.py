"""
prompt_corpus_loader.py

define ``load_corpus_tree`` and ``get_corpus_tree`` -- a name-keyed
cache of parsed prompt corpus trees -- plus ``get_default_corpus_tree``,
resolving whichever tree was loaded with ``is_default_tree=True``
"""

import re

from .prompt_corpus_node import PromptCorpusNode
from .dynamic_nodes import DYNAMIC_NODE_TYPES

__all__ = (
    "load_corpus_tree",
    "get_corpus_tree",
    "get_default_corpus_tree",
)


# constants  ###################################################################
ROOT_NODE_NAME = "○"


# auxiliaries  #################################################################


def _match_dynamic_node_type(heading):
    """
    :param heading: a section heading, as parsed from ``prompt_corpus.md``
    :type heading: str
    :return: the ``DYNAMIC_NODE_TYPES`` member ``heading`` refers to,
            or ``None`` if ``heading`` is an ordinary static heading
    :rtype: type or None
    :raises ValueError: ``heading`` is wrapped in parentheses but
            matches no known dynamic node type
    """
    if not (heading.startswith("(") and heading.endswith(")")):
        return None

    for node_type in DYNAMIC_NODE_TYPES:
        if heading == "(" + node_type.HEADING + ")":
            return node_type

    raise ValueError(
        "unrecognized dynamic node heading: {}".format(heading)
    )


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
            parentheses that matches no known dynamic node type
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
    for child in list(tree.children):
        node_type = _match_dynamic_node_type(child.name)
        if node_type is not None:
            prefaces[node_type] = tuple(child.content_lines())
            child.parent = None

    for node_type in DYNAMIC_NODE_TYPES:
        node_type(tree, preface=prefaces.get(node_type, ()))

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
