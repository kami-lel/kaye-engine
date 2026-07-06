"""
prompt_corpus_loader.py

define ``load_prompt_corpus_tree``
and its supporting function ``get_embedded_prompt_corpus_file_path()``
"""

import re
from pathlib import Path

from .prompt_corpus_node import PromptCorpusNode
from .sidecar_nodes import SidecarNode, SidecarNodeType
from .dynamic_nodes import DYNAMIC_NODE_TYPES

__all__ = (
    "get_embedded_prompt_corpus_file_path",
    "load_prompt_corpus_tree",
)


def get_embedded_prompt_corpus_file_path():
    """
    :return: absolute path of embedded prompt corpus ``prompt_corpus.md`` file
    :rtype: Path
    """
    return (
        Path(__file__).resolve().parent.parent / "prompt_corpus.md"
    ).absolute()


# singleton prompt corpus tree
prompt_corpus_tree = None  # pylint: disable=invalid-name


def load_prompt_corpus_tree():
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
    prompt_corpus_tree = _create_prompt_corpus_node_from_text_lines_recursively(
        ROOT_NODE_NAME, None, text_lines
    )

    # add dynamic nodes  -------------------------------------------------------
    for node_type in DYNAMIC_NODE_TYPES:
        node_type(prompt_corpus_tree)

    return prompt_corpus_tree


# helpers  #####################################################################
ROOT_NODE_NAME = "○"
HEADING_PREFIX_ELEMENT = "#"


def _is_sidecar_node_heading(heading):
    """
    check if a heading matches any sidecar node type

    :param heading: node name/heading to check
    :type heading: str
    :return: ``True`` if heading is a sidecar node
    :rtype: bool
    """
    for flag in SidecarNodeType:
        if flag and flag != SidecarNodeType.NONE:
            try:
                if heading == flag.as_node_heading:
                    return True
            except ValueError:
                # combined flags have no heading
                pass
    return False


def _create_prompt_corpus_node_from_text_lines_recursively(
    name, parent, text_lines
):
    # find every sub-section heading lines
    prefix_element_cnt = 1 if parent is None else parent.depth + 2
    heading_prefix = HEADING_PREFIX_ELEMENT * prefix_element_cnt + " "
    heading_lines_idx = []
    for idx, line in enumerate(text_lines):
        if line.startswith(heading_prefix):
            heading_lines_idx.append(idx)

    if heading_lines_idx:
        # contains subsections  ------------------------------------------------

        # get content_lines of current node level
        content_lines = text_lines[: heading_lines_idx[0]]
        node_class = (
            SidecarNode if _is_sidecar_node_heading(name) else PromptCorpusNode
        )
        node = node_class(name, parent, content_lines)

        # parse sub-sections, create children nodes
        for start, end in zip(
            heading_lines_idx, heading_lines_idx[1:] + [len(text_lines)]
        ):
            # extract heading content
            # e.g. "### this is heading " -> "this is heading"
            child_heading = text_lines[start][len(heading_prefix) :].strip()
            child_text_lines = text_lines[start + 1 : end]
            _create_prompt_corpus_node_from_text_lines_recursively(
                child_heading, node, child_text_lines
            )

        return node

    else:
        # contains no subsection  ----------------------------------------------
        # i.e. all of text_lines are node content
        node_class = (
            SidecarNode if _is_sidecar_node_heading(name) else PromptCorpusNode
        )
        return node_class(name, parent, text_lines)
