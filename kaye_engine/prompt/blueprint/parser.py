"""
parser.py

define ``parse_blueprint_text``
"""

import re

from .data import Blueprint
from .index import get_corpus_index

__all__ = ("HEADING_LINE_PATTERN", "parse_blueprint_text")


# constants  ###################################################################
HEADING_LINE_PATTERN = re.compile(r"\[([x ])\] (.*)[└├]── (.+)")


# auxiliaries  #################################################################
def _validate_against_corpus(path, line):
    """
    check ``path`` names a node of the loaded corpus; does nothing while
    no corpus is loaded, since the text alone carries no corpus

    (helper function used in ``parse_blueprint_text()``)
    """
    try:
        index = get_corpus_index()
    except ValueError:
        return

    if path in index.idx_by_path:
        return

    # name the first heading along the path the corpus does not know
    for depth in range(1, len(path) + 1):
        if path[:depth] not in index.idx_by_path:
            raise ValueError(
                "missing node heading {} in corpus "
                "that corresponds to this line:\n{}".format(
                    repr(path[depth - 1]), line
                )
            )


# Public API  ##################################################################
def parse_blueprint_text(blueprint_text):
    """
    parse ``blueprint_text`` into a blueprint of its checkmarked nodes

    ``blueprint_text`` must be in the same format as the output of
    ``render.render_blueprint_tree()`` (with tree structure and
    checkmarks); unchecked lines select nothing and are ignored. While a
    corpus is loaded, every heading is also checked against it


    :param blueprint_text: prompt blueprint text to set nodes
    :type blueprint_text: str
    :raise ValueError: malformed tree format, or a heading the loaded
            corpus does not contain
    :return: a blueprint whose ``nodes`` are the checkmarked lines' paths
    :rtype: Blueprint
    """
    nodes = set()

    # extract all headings  ----------------------------------------------------
    lineage = []
    for line in blueprint_text.split("\n"):
        heading_line_match = HEADING_LINE_PATTERN.fullmatch(line)

        if not heading_line_match:
            continue  # skip line that is not a node heading

        # extract info for current node
        is_checkmarked = heading_line_match.group(1) == "x"
        level = len(heading_line_match.group(2)) // 4 + 1
        heading = heading_line_match.group(3)

        # a node sits at most 1 level below the previous node
        if level - 1 > len(lineage):
            raise ValueError("malformed tree format at line:\n{}".format(line))

        lineage = lineage[: level - 1] + [heading]
        path = tuple(lineage)

        _validate_against_corpus(path, line)

        if is_checkmarked:
            nodes.add(path)

    return Blueprint(nodes=frozenset(nodes))
