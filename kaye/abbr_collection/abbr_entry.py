"""
abbr_entry.py

define ``AbbrEntry``
"""

from kaye.abbr_collection.abbr_tags import AbbrTags
from kaye.abbr_collection.abbr_wrap import AbbrWrap

# abbrs.json key constants  ####################################################

ABBRS_JSON_PRIORITY_KEY = "priority"
ABBRS_JSON_TAGS_KEY = "tags"
ABBRS_JSON_WRAP_KEY = "wrap"


# AbbrEntry  ###################################################################


class AbbrEntry:
    """
    represent an abbr => meaning structure


    :raises ValueError:
    """

    # instance structure  ******************************************************

    __slots__ = ("abbr", "mean", "priority", "tags", "wrap")

    def __init__(self, mean, abbr, abbr_obj):
        self.mean = mean  # referenced to meaning

        # set .abbr  -----------------------------------------------------------
        if not isinstance(abbr, str):
            raise ValueError("abbr key must be String: {}".format(repr(abbr)))
        self.abbr = abbr

        # test abbr_obj shapes  ------------------------------------------------
        if not isinstance(abbr_obj, dict):
            raise ValueError(
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
            raise ValueError(
                "priority must be Integer: {}".format(repr(priority))
            )
        self.priority = priority

        # set .tags  -----------------------------------------------------------
        self.tags = AbbrTags.parse(abbr_obj[ABBRS_JSON_TAGS_KEY])

        # set .wrap  -----------------------------------------------------------
        # may raise ValueError
        self.wrap = AbbrWrap(abbr_obj[ABBRS_JSON_WRAP_KEY])

    # instance methods  ********************************************************

    def as_md_list_entry(self):
        """
        render this entry as a markdown list item

        :return: a single markdown list item in the form
                ``- abbr:meaning``
        :rtype: str
        """
        return "- {}:{}".format(self.abbr, self.mean)

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
