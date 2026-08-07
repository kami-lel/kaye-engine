"""
abbr_entry.py

define ``AbbrEntry``
"""

from kaye_engine.abbr_collection.abbr_glossary import ABBRS_JSON_GLOSSARY_KEY
from kaye_engine.abbr_collection.abbr_tags import AbbrTags
from kaye_engine.abbr_collection.abbr_wrap import AbbrWrap

# abbrs.json key constants  ####################################################

ABBRS_JSON_PRIORITY_KEY = "priority"
ABBRS_JSON_TAGS_KEY = "tags"
ABBRS_JSON_WRAP_KEY = "wrap"
ABBRS_JSON_REMARK_KEY = "remark"


# AbbrEntry  ###################################################################


class AbbrEntry:
    """
    represent an abbr => meaning structure


    :raises TypeError:
    :raises ValueError:
    """

    # instance structure  ******************************************************

    __slots__ = (
        "abbr",
        "glossaries",
        "mean",
        "priority",
        "remark",
        "tags",
        "wrap",
    )

    def __init__(self, mean, abbr, abbr_obj):
        self.mean = mean  # referenced to meaning

        # set .abbr  -----------------------------------------------------------
        if not isinstance(abbr, str):
            raise TypeError("abbr key must be String: {}".format(repr(abbr)))
        self.abbr = abbr

        # test abbr_obj shapes  ------------------------------------------------
        if not isinstance(abbr_obj, dict):
            raise TypeError(
                "abbr value must be Object: {}".format(repr(abbr_obj))
            )
        missing_keys = [
            key
            for key in (
                ABBRS_JSON_PRIORITY_KEY,
                ABBRS_JSON_TAGS_KEY,
                ABBRS_JSON_WRAP_KEY,
            )
            if key not in abbr_obj
        ]
        if missing_keys:
            raise ValueError(
                "abbr value must contains key: {}".format(missing_keys)
            )

        # set .priority  -------------------------------------------------------
        priority = abbr_obj[ABBRS_JSON_PRIORITY_KEY]
        if not isinstance(priority, int):
            raise TypeError(
                "priority must be Integer: {}".format(repr(priority))
            )
        self.priority = priority

        # set .tags  -----------------------------------------------------------
        self.tags = AbbrTags.parse(abbr_obj[ABBRS_JSON_TAGS_KEY])

        # set .glossaries  -------------------------------------------------------
        # optional; free-form, consumer-defined glossary names, no fixed enum
        glossaries = abbr_obj.get(ABBRS_JSON_GLOSSARY_KEY, [])
        if not isinstance(glossaries, list) or not all(
            isinstance(glossary, str) for glossary in glossaries
        ):
            raise ValueError(
                "glossaries value must be Array of String: {}".format(
                    repr(glossaries)
                )
            )
        self.glossaries = tuple(glossaries)

        # set .wrap  -----------------------------------------------------------
        # may raise ValueError
        self.wrap = AbbrWrap(abbr_obj[ABBRS_JSON_WRAP_KEY])

        # set .remark  -----------------------------------------------------------
        remark = abbr_obj.get(ABBRS_JSON_REMARK_KEY)
        if remark is not None and not isinstance(remark, str):
            raise ValueError("remark must be String: {}".format(repr(remark)))
        self.remark = remark

    # instance methods  ********************************************************

    def as_md_list_entry(self, number=None):
        """
        render this entry as a markdown list item

        :param number: numbered list item instead of a bullet, if given
        :type number: int, optional
        :return: a single markdown list item
        :rtype: str
        """
        marker = "-" if number is None else "{}.".format(number)

        remarks = [r for r in (self.mean.remark, self.remark) if r]
        if remarks:
            return "{} {}:{} ({})".format(
                marker, self.abbr, self.mean, "; ".join(remarks)
            )
        return "{} {}:{}".format(marker, self.abbr, self.mean)

    def verify_found(self, found, char_before, char_after):
        """
        :param found:
        :type found: str
        :param char_before: single character immediately before the found;
                `""` if start of text
        :type char_before: str
        :param char_after: single character immediately after the found;
                `""` if end of text
        :type char_after: str
        :return: whether ``found`` satisfies additional rules of:

        - case sensitivity
        - wrapping

        :rtype: bool
        """
        return (
            self.abbr.islower() or found == self.abbr  # verify case sensitivity
        ) and self.wrap.is_satisfied_wrap_rule(char_before, char_after)

    # magic methods  ***********************************************************

    def __hash__(self):
        key = (self.abbr, self.mean)
        return hash(key)

    def __eq__(self, other):
        if not isinstance(other, AbbrEntry):
            return NotImplemented

        return self.abbr == other.abbr and self.mean == other.mean

    def __repr__(self):
        return "{}:{}".format(self.abbr, self.mean)
