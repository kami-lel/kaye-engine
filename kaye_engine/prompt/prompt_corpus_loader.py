"""
prompt_corpus_loader.py

define ``load_corpus_tree`` and ``get_corpus_tree`` -- a name-keyed
cache of parsed prompt corpus trees -- plus ``load_prompt_corpus_tree``
and ``get_embedded_prompt_corpus_file_path()``, kept as back-compat
wrappers around a single ``"default"`` named tree
"""

import re
from pathlib import Path

from .prompt_corpus_node import PromptCorpusNode
from .dynamic_nodes import DYNAMIC_NODE_TYPES

__all__ = (
    "get_embedded_prompt_corpus_file_path",
    "load_prompt_corpus_tree",
    "load_corpus_tree",
    "get_corpus_tree",
)


# constants  ###################################################################
ROOT_NODE_NAME = "○"


# auxiliaries  #################################################################


def _attach_dynamic_node(parent, node_type):
    """
    attach a ``node_type`` instance under ``parent``;
    if a statically-authored ``PromptCorpusNode`` with the same heading
    already exists among ``parent``'s children, detach it and carry its
    content over as the dynamic node's ``preface``
    """
    heading = "(" + node_type.HEADING + ")"

    preface = ()
    for child in parent.children:
        if child.name == heading:
            preface = tuple(child.content_lines())
            child.parent = None
            break

    node_type(parent, preface=preface)


# name-keyed cache of parsed prompt corpus trees
_corpus_tree_cache = {}


# Public API  ##################################################################


def get_embedded_prompt_corpus_file_path():  # =================================
    """
    :return: absolute path of embedded prompt corpus ``prompt_corpus.md`` file
    :rtype: Path
    """
    return (
        Path(__file__).resolve().parent.parent / "prompt_corpus.md"
    ).absolute()


def load_corpus_tree(tree_name, file_path):  # ==================================
    """
    parse ``file_path`` into a **prompt corpus tree** and cache it under
    ``tree_name``, attaching the various dynamic nodes once


    :param tree_name: key this tree is cached under; every subsequent
            :func:`get_corpus_tree` call with this name returns the
            same tree object
    :type tree_name: str
    :param file_path: path of the markdown file to parse
    :type file_path: Path or str
    :raises ValueError: ``tree_name`` is already registered
    :raises FileNotFoundError:
    :raises IOError:
    :return: **root** node of the parsed *prompt corpus tree*
    :rtype: PromptCorpusNode
    """
    if tree_name in _corpus_tree_cache:
        raise ValueError(
            "duplicate corpus tree name: {}".format(tree_name)
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
    for node_type in DYNAMIC_NODE_TYPES:
        _attach_dynamic_node(tree, node_type)

    _corpus_tree_cache[tree_name] = tree
    return tree


def get_corpus_tree(tree_name):  # ==============================================
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


def load_prompt_corpus_tree():  # ==============================================
    """
    get the **default** *prompt corpus tree* singleton -- a thin
    back-compat wrapper around :func:`load_corpus_tree` /
    :func:`get_corpus_tree` using the reserved name ``"default"``

    :raises FileNotFoundError:
    :raises IOError:
    :return: **root** node of *prompt corpus tree*
    :rtype: PromptCorpusNode
    """
    try:
        return get_corpus_tree("default")
    except KeyError:
        return load_corpus_tree(
            "default", get_embedded_prompt_corpus_file_path()
        )
