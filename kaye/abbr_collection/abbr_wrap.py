"""
abbr_wrap.py

define ``AbbrWrap`` and its boundary patterns
"""

import re
from enum import Enum


# patterns  ####################################################################

WORD_BOUNDARY_PATTERN = re.compile(r"\s|[^\w]?")
NUMBER_OR_BOUNDARY_PATTERN = re.compile(r"\s|[0-9]?")
WORD_PATTERN = re.compile(r"\w")


# AbbrWrap  ####################################################################


class AbbrWrap(Enum):
    """
    represent an abbr wrap type as ``Enum``
    """

    # enum instances  ==========================================================

    WORD = "word"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    SYMBOL = "symbol"
    UNIT = "unit"
    CURRENCY = "currency"

    # instance methods  ========================================================

    def is_satisfied_wrap_rule(self, char_before, char_after):
        """
        :param char_before: single character immediately before the found;
                `""` if start of text
        :type char_before: str
        :param char_after: single character immediately after the found;
                `""` if end of text
        :type char_after: str
        """

        if self == AbbrWrap.WORD:
            return WORD_BOUNDARY_PATTERN.fullmatch(
                char_before
            ) and WORD_BOUNDARY_PATTERN.fullmatch(char_after)

        elif self == AbbrWrap.PREFIX:
            return WORD_BOUNDARY_PATTERN.fullmatch(
                char_before
            ) and WORD_PATTERN.fullmatch(char_after)

        elif self == AbbrWrap.SUFFIX:
            return WORD_PATTERN.fullmatch(
                char_before
            ) and WORD_BOUNDARY_PATTERN.fullmatch(char_after)

        elif self == AbbrWrap.SYMBOL:
            return True

        elif self == AbbrWrap.UNIT:
            return NUMBER_OR_BOUNDARY_PATTERN.fullmatch(
                char_before
            ) and WORD_BOUNDARY_PATTERN.fullmatch(char_after)

        elif self == AbbrWrap.CURRENCY:
            return WORD_BOUNDARY_PATTERN.fullmatch(
                char_before
            ) and NUMBER_OR_BOUNDARY_PATTERN.fullmatch(char_after)

        raise NotImplementedError
