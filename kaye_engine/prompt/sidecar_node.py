"""
sidecar_node.py

nodes attached to a blueprint's parent node but stored as corpus content,
identified by the ``{name}`` heading convention; excluded by default and
conditionally spliced in via ``contains_sidecars`` when their parent is
checkmarked
"""

import re

from kaye_engine.prompt import REPLACEMENT_NEWLINE_SYMBOL

__all__ = (
    "get_sidecar_name",
    "BlueprintDescriptorSidecars",
)

# reserved descriptor names, documentation only; consumption is by string key
DESCRIPTION_NAME = "description"
WHEN_TO_USE_NAME = "when_to_use"
GLOBS_NAME = "globs"


# name detection  ##############################################################

_SIDECAR_HEADING_PATTERN = re.compile(r"^\{(.+)\}$")


def get_sidecar_name(node):
    """
    determine a node's sidecar name from its heading

    identifies a sidecar node by its ``{name}`` heading convention and
    returns the name inside the braces (e.g., ``description``,
    ``globs``). returns ``None`` if the node is not a sidecar node.

    **usage**:

    >>> from kaye_engine.prompt.sidecar_node import get_sidecar_name
    >>> name = get_sidecar_name(node)
    >>> if name is not None:
    ...     print(f"sidecar name: {name}")
    >>> if name == "for claude code":
    ...     print("this is a conditional sidecar node")


    :param node: node to check (must have a ``name`` attribute)
    :type node: BasePromptNode
    :return: the sidecar name, or ``None`` if not a sidecar node
    :rtype: str or None
    """
    match = _SIDECAR_HEADING_PATTERN.match(node.name)
    return match.group(1) if match else None


class BlueprintDescriptorSidecars:  ############################################
    """
    blueprint description sidecar node lookups
    (description, when_to_use, globs)


    :param main_node: blueprint node that may contain descriptor sidecars
    :type main_node: BasePromptNode or None
    """

    @property
    def description(self):
        """
        retrieve the description text

        :return: description text, or rendered description node content
        :rtype: str
        """
        return self._description or REPLACEMENT_NEWLINE_SYMBOL.join(
            self._convert_node2content_lines(self.description_node)
        )

    @description.setter
    def description(self, value):
        """
        set the description text

        :param value: new description text
        :type value: str
        """
        self._description = value

    @property
    def when_to_use(self):
        """
        retrieve the when-to-use text

        :return: rendered when-to-use node content
        :rtype: str
        """
        return REPLACEMENT_NEWLINE_SYMBOL.join(
            self._convert_node2content_lines(self.when_to_use_node)
        )

    @property
    def description_and_when_to_use(self):
        """
        retrieve the combined description and when-to-use text

        :return: rendered description and when-to-use content
        :rtype: str
        """
        return self._description or REPLACEMENT_NEWLINE_SYMBOL.join(
            self._convert_node2content_lines(self.description_node)
            + self._convert_node2content_lines(self.when_to_use_node)
        )

    @property
    def globs(self):
        """
        retrieve glob patterns

        :return: glob patterns extracted from the sidecar node content
        :rtype: list[str]
        """
        lines = self._convert_node2content_lines(self.globs_node)

        results = []
        in_block = False

        for line in lines:
            if line == "```glob":
                in_block = True
                continue

            if line == "```" and in_block:
                break

            if in_block:
                results.append(line)

        return results

    # constructor  ===============================================================

    def __init__(self, *, main_node=None):
        self._description = None
        self.description_node = None
        self.when_to_use_node = None
        self.globs_node = None

        if main_node:
            try:
                self.description_node = main_node[
                    "{{{}}}".format(DESCRIPTION_NAME)
                ]
            except KeyError:
                pass

            try:
                self.when_to_use_node = main_node[
                    "{{{}}}".format(WHEN_TO_USE_NAME)
                ]
            except KeyError:
                pass

            try:
                self.globs_node = main_node["{{{}}}".format(GLOBS_NAME)]
            except KeyError:
                pass

    # operator  ===================================================================

    def __or__(self, other):
        """
        merge two BlueprintDescriptorSidecars; left takes priority

        :param other: right operand
        :type other: BlueprintDescriptorSidecars
        :return: merged description sidecars
        :rtype: BlueprintDescriptorSidecars
        """
        merged = BlueprintDescriptorSidecars()
        merged._description = self._description or other._description
        merged.description_node = (
            self.description_node or other.description_node
        )
        merged.when_to_use_node = (
            self.when_to_use_node or other.when_to_use_node
        )
        merged.globs_node = self.globs_node or other.globs_node
        return merged

    # helpers  =====================================================================

    @staticmethod
    def _convert_node2content_lines(node):
        """
        render a node into prompt content lines

        :param node: node to render
        :type node: BasePromptNode or None
        :return: rendered prompt lines
        :rtype: list[str]
        """
        if not node:
            return []

        from kaye_engine.prompt.blueprint import PromptBlueprint, render

        bp = PromptBlueprint.create_from_node(node, corpus_tree=node.root)
        return render.render_prompt_lines(bp, disable_first_heading=True)
