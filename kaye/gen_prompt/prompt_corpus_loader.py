"""
define ``spawn_prompt_corpus_tree``
and its supporting function ``get_embedded_prompt_corpus_file_path()``
"""

import re
from pathlib import Path


from .prompt_corpus_node import PromptCorpusNode
from .today_node import TodayNode
from .abbr_nodes import AbbrNode, PLCNode

__all__ = (
    "get_embedded_prompt_corpus_file_path",
    "spawn_prompt_corpus_tree",
)


def get_embedded_prompt_corpus_file_path():
    """
    :return: absolute path of embedded prompt corpus ``prompt_corpus.md`` file
    :rtype: Path
    """
    return (
        Path(__file__).resolve().parent.parent / "prompt_corpus.md"
    ).absolute()


def spawn_prompt_corpus_tree(
    *, prompt_corpus_text_override=None, disable_dynamic_nodes=False
):
    """
    create the **prompt corpus tree** by:

    - parse the prompt corpus text saved in ``prompt_corpus.md``
    - attach various dynamic nodes


    :param prompt_corpus_text_override: (for test); default to None
    :type prompt_corpus_text_override: str, optional
    :param disable_dynamic_nodes: (for test); defaults to False
    :type disable_dynamic_nodes: bool, optional
    :raises FileNotFoundError:
    :raises IOError:
    :return: **root** node of *prompt corpus tree*
    :rtype: PromptCorpusNode
    """
    if prompt_corpus_text_override is None:
        # read corpus from file  -----------------------------------------------
        prompt_corpus_file_path = get_embedded_prompt_corpus_file_path()
        with open(
            prompt_corpus_file_path, "r", encoding="utf-8", newline=""
        ) as file:
            prompt_corpus_text = file.read()

    else:
        prompt_corpus_text = prompt_corpus_text_override

    # text split & clean up  ---------------------------------------------------
    # reduce 2+ empty lines into single empty line
    text_cleanup = re.sub(r"\n{3,}", "\n\n", prompt_corpus_text)
    # split to lines
    text_lines = list(text_cleanup.split("\n"))

    # create prompt corpus nodes  ----------------------------------------------
    root = _create_prompt_corpus_node_from_text_lines_recursively(
        ROOT_NODE_NAME, None, text_lines
    )

    # attach dynamic nodes  ----------------------------------------------------
    if not disable_dynamic_nodes:
        TodayNode(root)
        AbbrNode(root)
        PLCNode(root)

    return root


# helpers  #####################################################################
ROOT_NODE_NAME = "○"
HEADING_PREFIX_ELEMENT = "#"


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
        node = PromptCorpusNode(name, parent, content_lines)

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
        return PromptCorpusNode(name, parent, text_lines)
