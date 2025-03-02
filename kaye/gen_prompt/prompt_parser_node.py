import re
from collections import OrderedDict

LF = "\n"
HEADING_MARKER = "#"


class PromptParserNode(OrderedDict):

    def __str__(self):
        """
        :return: rendered ``.md`` content,
        when conisder ``.enable`` of current node and sub-nodes
        :rtype: str
        """
        parts = [self.content]

        for heading, node in self.items():
            if node.enable:
                heading_md = HEADING_MARKER * node.level + " " + heading + LF
                part = heading_md + node.__str__()
                parts.append(part)

        return LF.join(parts)

    def __repr__(self, heading=""):
        """
        debug print of _PromptTreeNode, showing

        - node enable by ☑ or ☐
        - node content as 1st entry
        - heading & content of its sub-nodes
        """
        tab_prefix = "\t" * self.level

        first_line = (
            ("☑" if self.enable else "☐")
            + tab_prefix
            + HEADING_MARKER * self.level
            + " "
            + heading
            + " "
            + "{"
        )

        content_line = repr(self.content[:64])

        nodes_repr = LF.join(
            node.__repr__(heading) for heading, node in self.items()
        )

        last_line = "}"

        if nodes_repr:
            content_line = tab_prefix + content_line
            last_line = tab_prefix + last_line
            return LF.join([first_line, content_line, nodes_repr, last_line])
        else:
            return first_line + content_line + last_line

    def set_recursively(self):
        """
        enable this node (& its sub-nodes) to be present
        during ``.md`` render (q.v. ``__str__``)
        """
        self._set_unset_recursively(True)

    def unset_recursively(self):
        """
        disable this node (& its sub-nodes) to be absent
        during ``.md`` render (q.v. ``__str__``)
        """
        self._set_unset_recursively(False)

    def __new__(cls, text, parent=None):
        return super().__new__(cls, {})  # new as empty dict

    def __init__(self, text, parent=None):
        self.parent = parent
        self.content = ""
        self.enable = True

        if parent is None:  # when current node is root
            self.level = 0
            text = self._convert_full_prompt2text_list(text)
        else:
            self.level = parent.level + 1

        self._init_populate_by_text_list(text)

    @staticmethod
    def _convert_full_prompt2text_list(full_prompt):
        """
        :param full_prompt: The full prompt string to be converted.
        :type full_prompt: str
        :return: A list of lines from the cleaned-up prompt string.
        :rtype: list(str)
        """
        # remove all empty lines
        cleanup = re.sub(rf"{LF}+", LF, full_prompt)
        return list(cleanup.split(LF))

    def _init_populate_by_text_list(self, lines):
        heading_prefix = HEADING_MARKER * (self.level + 1) + " "

        # find every sub-section heading lines
        heading_lines = []
        for idx, line in enumerate(lines):
            if line.startswith(heading_prefix):
                heading_lines.append(idx)

        if not heading_lines:  # contain no subsection
            self.content = LF.join(lines)  # all lines are content
            return

        # this node contains subsections
        # parse the content part out
        self.content = LF.join(lines[: heading_lines[0]])

        # parse sub-sections as nodes
        heading_lines.append(len(lines))
        for start, end in zip(heading_lines, heading_lines[1:]):
            # extract heading content
            # e.g. "### this is heading " -> "this is heading"
            heading_content = lines[start][len(heading_prefix) :].strip()
            self[heading_content] = PromptParserNode(
                lines[start + 1 : end], self
            )

    def _set_unset_recursively(self, enable):
        self.enable = enable

        # make sure all parent & grandparents enabled
        parent = self.parent
        while parent is not None:
            parent.enable = enable
            parent = parent.parent

        # make all children & grandchilrens enabled
        for _, node in self.items():
            node._set_unset(enable)
