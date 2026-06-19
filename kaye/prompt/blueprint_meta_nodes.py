"""
blueprint_meta_fields.py

define ``BlueprintMetaNodes`` and ``collapse_lines_into_single_line``
"""

from kaye.prompt.meta_node_type import MetaNodeType

REPLACEMENT_NEWLINE_SYMBOL = "↵"  # HACK replace


def collapse_lines_into_single_line(lines):
    """
    collapse an iterable of text lines into one single-line string


    :param lines: the text lines to collapse onto a single line
    :type lines: Iterable[str]
    :return: the lines joined into one string by the line-break glyph
    :rtype: str
    """
    return REPLACEMENT_NEWLINE_SYMBOL.join(lines)


class BlueprintMetaNodes:  #####################################################
    """
    blueprint meta node lookups


    :param main_node: blueprint node that may contain meta subnodes
    :type main_node: BasePromptNode or None
    """

    @property
    def description(self):
        """
        retrieve the description text for the blueprint meta node

        :return: description text, or rendered description node content
        :rtype: str
        """
        return self._description or collapse_lines_into_single_line(
            self._convert_node2content_lines(self.description_node)
        )

    @description.setter
    def description(self, value):
        """
        set the description text for the blueprint meta node

        :param value: new description text
        :type value: str
        """
        self._description = value

    @property
    def when_to_use(self):
        """
        retrieve the when-to-use text for the blueprint meta node

        :return: rendered when-to-use node content
        :rtype: str
        """
        return collapse_lines_into_single_line(
            self._convert_node2content_lines(self.when_to_use_node)
        )

    @property
    def description_and_when_to_use(self):
        """
        retrieve the combined description and when-to-use text

        :return: rendered description and when-to-use content
        :rtype: str
        """
        return self._description or collapse_lines_into_single_line(
            self._convert_node2content_lines(self.description_node)
            + self._convert_node2content_lines(self.when_to_use_node)
        )

    @property
    def globs(self):
        """
        retrieve glob patterns from the blueprint meta node

        :return: glob patterns extracted from the meta node content
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

    # constructor  =============================================================

    def __init__(self, *, main_node=None):
        self._description = None
        self.description_node = None
        self.when_to_use_node = None
        self.globs_node = None
        self.prerequisite_node = None

        if main_node:
            try:
                self.description_node = main_node[
                    MetaNodeType.DESCRIPTION.as_node_heading
                ]
            except KeyError:
                pass

            try:
                self.when_to_use_node = main_node[
                    MetaNodeType.WHEN_TO_USE.as_node_heading
                ]
            except KeyError:
                pass

            try:
                self.globs_node = main_node[MetaNodeType.GLOBS.as_node_heading]
            except KeyError:
                pass

            try:
                self.prerequisite_node = main_node[
                    MetaNodeType.PREREQUISITE.as_node_heading
                ]
            except KeyError:
                pass

    # helpers  =================================================================

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

        from kaye.prompt.prompt_blueprint import PromptBlueprint

        bp = PromptBlueprint.create_from_node(node)
        return bp.generate_prompt_lines(disable_first_heading=True)
