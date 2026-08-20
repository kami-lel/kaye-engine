"""
dynamic_substitution.py

define ``apply_dynamic_substitutions`` -- a render-time
search-and-replace pass resolving inline ``(((name)))`` placeholders
against the same canonical dynamic node universe as the tree
mechanism, independent of checkmarking
"""

import re

from kaye_engine import LOGGER_NAME, kamilog
from kaye_engine.prompt.dynamic_nodes import resolve_dynamic_node_factory

__all__ = ("apply_dynamic_substitutions",)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# constants  ###################################################################
PLACEHOLDER_PATTERN = re.compile(r"\(\(\(([^()]+)\)\)\)")


# Public API  ##################################################################
def apply_dynamic_substitutions(text, **kwargs):
    """
    replace every ``(((name)))`` placeholder in ``text`` with the
    rendered content of the dynamic node ``name`` resolves to via
    :func:`resolve_dynamic_node_factory`, using a headless instance
    (``parent=None``, empty preface) -- an unresolved ``name`` logs a
    warning and leaves the literal ``(((name)))`` text in place


    :param text: fully-assembled prompt text to search & replace within
    :type text: str
    :param kwargs: forwarded to each resolved node's ``content_lines()``
            (e.g. ``query``, ``glossary_priority_threshold``)
    :return: ``text`` with every resolvable placeholder substituted
    :rtype: str
    """
    cache = {}

    def _replace(match):
        name = match.group(1).strip()
        if name not in cache:
            try:
                factory = resolve_dynamic_node_factory(name)
                node = factory(parent=None)
                cache[name] = "\n".join(node.content_lines(**kwargs))
            except ValueError:
                logger.warning(
                    "unresolved dynamic substitution placeholder: %s", name
                )
                cache[name] = match.group(0)
        return cache[name]

    return PLACEHOLDER_PATTERN.sub(_replace, text)
