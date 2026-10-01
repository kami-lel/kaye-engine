"""
render.meta.py

define ``render_description``, ``render_when_to_use``,
``render_description_and_when_to_use``, ``extract_globs`` -- what the
skill and rule exporters read from a blueprint's ``meta``
"""

from ..index import BlueprintSelection, get_corpus_index
from ..render_profile import RenderProfile
from .lines import render_prompt_lines
from .util import REPLACEMENT_NEWLINE_SYMBOL

__all__ = (
    "extract_globs",
    "render_description",
    "render_description_and_when_to_use",
    "render_when_to_use",
)


# auxiliaries  #################################################################
def _render_node_lines(path, *, sparseness):
    """
    :param path: path of the node to render, ``None`` for no node
    :type path: NodePath or None
    :return: the node's own content lines, no heading
    :rtype: list[str]
    """
    if path is None:
        return []

    index = get_corpus_index()
    try:
        idx = index.idx_by_path[path]
    except KeyError as err:
        raise ValueError(
            "no node in corpus at path: {}".format(list(path))
        ) from err

    return render_prompt_lines(
        BlueprintSelection(index, 1 << idx),
        profile=RenderProfile(
            disable_first_heading=True, sparseness=sparseness
        ),
    )


# Public API  ##################################################################
def render_description(blueprint):
    """
    :param blueprint:
    :type blueprint: Blueprint
    :raises ValueError: the description node is not in the loaded corpus
    :return: the literal description when set, else the description
            node's content as one line, else ``""``
    :rtype: str
    """
    if blueprint.meta.description:
        return blueprint.meta.description

    lines = _render_node_lines(blueprint.meta.description_node, sparseness=-1)
    return lines[0] if lines else ""


def render_when_to_use(blueprint):
    """
    :param blueprint:
    :type blueprint: Blueprint
    :raises ValueError: the when-to-use node is not in the loaded corpus
    :return: the when-to-use node's content as one line, else ``""``
    :rtype: str
    """
    lines = _render_node_lines(blueprint.meta.when_to_use_node, sparseness=-1)
    return lines[0] if lines else ""


def render_description_and_when_to_use(blueprint):
    """
    :param blueprint:
    :type blueprint: Blueprint
    :raises ValueError: a meta node is not in the loaded corpus
    :return: the literal description when set, else the description and
            when-to-use nodes' content joined by the replacement newline
            symbol
    :rtype: str
    """
    if blueprint.meta.description:
        return blueprint.meta.description

    return REPLACEMENT_NEWLINE_SYMBOL.join(
        _render_node_lines(blueprint.meta.description_node, sparseness=-1)
        + _render_node_lines(blueprint.meta.when_to_use_node, sparseness=-1)
    )


def extract_globs(blueprint):
    """
    :param blueprint:
    :type blueprint: Blueprint
    :raises ValueError: the globs node is not in the loaded corpus
    :return: glob patterns of the globs node's first fenced ``glob``
            block
    :rtype: list[str]
    """
    results = []
    in_block = False

    for line in _render_node_lines(blueprint.meta.globs_node, sparseness=1):
        if line == "```glob":
            in_block = True
            continue

        if line == "```" and in_block:
            break

        if in_block:
            results.append(line)

    return results
