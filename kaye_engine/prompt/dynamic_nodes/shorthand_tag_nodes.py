"""
shorthand_tag_nodes.py

define tag-filtered content for the decode-only abbr node
"""

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.abbr_collection import get_abbr_data

__all__ = ("gen_shorthand_content_lines",)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


def gen_shorthand_content_lines(abbr_tag):
    """
    :return: markdown list items for every ``get_abbr_data().abbrs``
            entry whose tags contain ``abbr_tag``; empty when the abbr
            data singleton is still empty
    :rtype: list[str]
    """
    abbr_data = get_abbr_data()
    if not abbr_data:
        logger.error("abbr data is empty, rendering without any abbr")
        return []

    lines = []
    for entry in abbr_data.abbrs:
        if abbr_tag in entry.tags:
            lines.append(entry.as_md_list_entry())
    return lines
