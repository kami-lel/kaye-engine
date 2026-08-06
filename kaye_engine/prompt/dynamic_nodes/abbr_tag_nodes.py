"""
abbr_tag_nodes.py

define abbreviation-tag-filtered node types
"""

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.abbr_collection import get_abbr_data

__all__ = ("gen_abbrs_content_lines",)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


# HACK duplicated fx
def gen_abbrs_content_lines(abbr_tag):
    """
    render every ``get_abbr_data().abbrs`` entry matching ``abbr_tag``
    as a list of markdown list items; empty when the abbr data singleton
    is still empty


    :param abbr_tag: tag to filter entries by
    :type abbr_tag: AbbrTags
    :return: rendered markdown list items, one per matching entry
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
