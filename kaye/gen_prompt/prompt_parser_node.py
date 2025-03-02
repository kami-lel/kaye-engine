import re
from collections import OrderedDict

LF = "\n"
HEADING_MARKER = "#"


class PromptParserNode(OrderedDict):

    def __str__(self):
        return ""  # TODO

    def __repr__(self):
        return ""  # TODO

    def __new__(cls, text, parent=None):
        return super().__new__(cls, {})  # new as empty dict

    def __init__(self, text, parent=None):
        self.parent = parent
        self.level = 0 if parent is None else parent.level + 1
        self.content = ""

        if parent is None:
            text = self._convert_full_prompt2text_list(text)

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
            heading_content = lines[start][len(heading_prefix) :].strip()
            self[heading_content] = PromptParserNode(
                lines[start + 1 : end], self
            )

            pass  # TODO
