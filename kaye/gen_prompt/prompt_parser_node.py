import re
from collections import OrderedDict

LF = "\n"
HEADING_MARKER = "#"


class PromptParserNode(OrderedDict):

    def __str__(self):
        return ""  # TODO

    def __repr__(self):
        return ""  # TODO

    def __new__(cls, level, parent, full_prompt):
        return super().__new__(cls, {})  # new as empty dict

    def __init__(self, text, parent=None, level=0):
        self.parent = parent
        self.level = level

        if level == 0:
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

        heading_lines.insert(0, 0)
        heading_lines.append(len(lines))
