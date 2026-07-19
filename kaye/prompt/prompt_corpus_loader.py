"""
prompt_corpus_loader.py

define ``load_prompt_corpus_tree``
and its supporting function ``get_embedded_prompt_corpus_file_path()``
"""

import re
from pathlib import Path

from .prompt_corpus_node import PromptCorpusNode
from .dynamic_nodes import DYNAMIC_NODE_TYPES

__all__ = (
    "get_embedded_prompt_corpus_file_path",
    "load_prompt_corpus_tree",
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


# singleton prompt corpus tree
prompt_corpus_tree = None  # pylint: disable=invalid-name


# Public API  ##################################################################


def get_embedded_prompt_corpus_file_path():  # =================================
    """
    :return: absolute path of embedded prompt corpus ``prompt_corpus.md`` file
    :rtype: Path
    """
    return (
        Path(__file__).resolve().parent.parent / "prompt_corpus.md"
    ).absolute()


def load_prompt_corpus_tree():  # ==============================================
    """
    get the **prompt corpus tree** *singleton*, which is created by:

    - parse the prompt corpus text saved in ``prompt_corpus.md``
    - attach various dynamic nodes


    :param prompt_corpus_text_override: (for testing only); default to None
    :type prompt_corpus_text_override: str, optional
    :raises FileNotFoundError:
    :raises IOError:
    :return: **root** node of *prompt corpus tree*
    :rtype: PromptCorpusNode
    """
    # prompt corpus tree singleton
    global prompt_corpus_tree  # pylint: disable=global-statement

    # early exit for singleton  ++++++++++++++++++++++++++++++++++++++++++++++++
    if prompt_corpus_tree is not None:
        return prompt_corpus_tree

    # create singleton  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # read corpus content from file
    prompt_corpus_file_path = get_embedded_prompt_corpus_file_path()
    with open(
        prompt_corpus_file_path, "r", encoding="utf-8", newline=""
    ) as file:
        prompt_corpus_text = file.read()

    # text split & clean up  ---------------------------------------------------
    # reduce 2+ empty lines into single empty line
    text_cleanup = re.sub(r"\n{3,}", "\n\n", prompt_corpus_text)
    # split to lines
    text_lines = list(text_cleanup.split("\n"))

    # create prompt corpus nodes  ----------------------------------------------
    prompt_corpus_tree = PromptCorpusNode.parse(
        ROOT_NODE_NAME, None, text_lines
    )

    # add dynamic nodes  -------------------------------------------------------
    for node_type in DYNAMIC_NODE_TYPES:
        _attach_dynamic_node(prompt_corpus_tree, node_type)

    return prompt_corpus_tree
