"""
parser.py

define ``parse_blueprint_text``
"""

import re

__all__ = ("HEADING_LINE_PATTERN", "parse_blueprint_text")


# constants  ###################################################################
HEADING_LINE_PATTERN = re.compile(r"\[([x ])\] (.*)[└├]── (.+)")


# auxiliaries  #################################################################
def _lookup_corpus_node(parent, heading, line):
    """
    find node under ``parent`` matching ``heading``

    (helper function used in ``parse_blueprint_text()``)
    """
    try:
        return parent[heading]
    except KeyError as err:
        raise ValueError(
            "missing node heading {} in corpus "
            "that corresponds to this line:\n{}".format(repr(heading), line)
        ) from err


# Public API  ##################################################################
def parse_blueprint_text(blueprint_text, corpus):
    """
    parse ``blueprint_text`` into a dict of checkmark state, keyed by
    node hash

    ``blueprint_text`` must be in the same format as the output of
    ``render.render_blueprint_tree()``
    (with tree structure and checkmarks)


    :param blueprint_text: prompt blueprint text to set nodes
    :type blueprint_text: str
    :param corpus: root of the corpus tree to resolve headings against
    :type corpus: BasePromptNode
    :raise ValueError:
    :return: dict of {node_hash: is_checkmarked}
    :rtype: dict(int, bool)
    """
    checkmarks = {}

    # extract all headings  ----------------------------------------------------
    prev_node = corpus
    for line in blueprint_text.split("\n"):
        heading_line_match = HEADING_LINE_PATTERN.fullmatch(line)

        if not heading_line_match:
            continue  # skip line that is not a node heading

        # extract info for current node
        is_checkmarked = heading_line_match.group(1) == "x"
        level = len(heading_line_match.group(2)) // 4 + 1
        heading = heading_line_match.group(3)

        # find parent of current node
        level_offset = level - prev_node.depth
        if level_offset > 1:
            raise ValueError("malformed tree format at line:\n{}".format(line))

        elif level_offset > 0:
            parent = prev_node

        else:
            parent = prev_node.ancestors[level - 1]

        # find current node in corpus
        node = _lookup_corpus_node(parent, heading, line)

        # include node in the checkmark state
        checkmarks[hash(node)] = is_checkmarked

        prev_node = node

    return checkmarks
