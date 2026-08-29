"""
abbr_entry.py

define ``AbbrEntry``
"""

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

        # set .tags & .glossaries  -----------------------------------------------
        # each "tags" entry is tried as an AbbrTags member first; on failure
        # it's treated as a free-form, consumer-defined glossary name instead,
        # validated later against the registry by AbbrData.add_entry
        tags_list = abbr_obj[ABBRS_JSON_TAGS_KEY]
        if not isinstance(tags_list, list):
            raise ValueError(
                "tags value must be Array: {}".format(repr(tags_list))
            )

        tags = AbbrTags.NONE
        glossaries = []
        for tag in tags_list:
            if not isinstance(tag, str):
                raise ValueError(
                    "tags entry must be String: {}".format(repr(tag))
                )
            try:
                tags |= AbbrTags[tag]
            except KeyError:
                glossaries.append(tag)
        self.tags = tags
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

    def as_md_list_entry(
        self, number=None, is_remark_disabled=False, force_term_definition=False
    ):
        """
        render this entry as a markdown list item

        :param number: numbered list item instead of a bullet, if given
        :type number: int, optional
        :param is_remark_disabled: omit the ``(...)`` remark suffix, even if
                `mean.remark` or `remark` are set; defaults to False
        :type is_remark_disabled: bool, optional
        :param force_term_definition: render as a term definition
                (``{mean}``, no ``{abbr}:`` prefix) even if this entry
                does not carry the ``term_definition`` tag; defaults to
                False
        :type force_term_definition: bool, optional
        :return: a single markdown list item
        :rtype: str
        """
        marker = "-" if number is None else "{}.".format(number)
        is_term_definition = (
            force_term_definition or AbbrTags.term_definition in self.tags
        )

        if not is_remark_disabled:
            remarks = [r for r in (self.mean.remark, self.remark) if r]
            if remarks:
                if is_term_definition:
                    return "{} {} ({})".format(
                        marker, self.mean, "; ".join(remarks)
                    )
                return "{} {}:{} ({})".format(
                    marker, self.abbr, self.mean, "; ".join(remarks)
                )
        if is_term_definition:
            return "{} {}".format(marker, self.mean)
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

        - not tagged ``term_definition``
        - case sensitivity
        - wrapping

        :rtype: bool
        """
        if AbbrTags.term_definition in self.tags:
            return False
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
