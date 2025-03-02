import re
from collections import OrderedDict

LF = "\n"
HEADING_MARKER = "#"


class PromptParserNode(OrderedDict):

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
        Convert the given full prompt string into a list of text lines.

        This method takes a full prompt string, cleans up any consecutive empty
        lines, and splits the string into a list of individual lines.

        :param full_prompt: The full prompt string to be converted.
        :type full_prompt: str
        :return: A list of lines from the cleaned-up prompt string.
        :rtype: list of str
        """
        # clean up consecutive empty lines
        # FIXME clean up pre- / post- heading empty line
        cleanup = re.sub(rf"{LF}+", LF, full_prompt)
        return list(cleanup.split(LF))

    def _init_populate_by_text_list(self, lines):
        heading_prefix = HEADING_MARKER * (self.level + 1) + " "

        # find every sub-section heading line
        heading_lines = OrderedDict()
        for idx, line in enumerate(lines):
            if line.startswith(heading_prefix):
                # extract heading content
                # e.g. "### this is heading " -> "this is heading"
                heading_content = line[len(heading_prefix) :].strip()
                heading_lines[idx] = heading_content

        # e.g. now, heading_lines = {0: 'personality',
        #       38: 'conversation', 95: 'abbreviation', 512: 'role'}
