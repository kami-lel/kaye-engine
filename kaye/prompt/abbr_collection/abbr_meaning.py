"""
abbr_meaning.py

define ``AbbrMeaning``
"""


class AbbrMeaning:
    """
    represent a single meaning (of possible different spellings)


    :raises ValueError:
    """

    __slots__ = ("mean",)

    def __init__(self, mean):
        if not isinstance(mean, str):
            raise ValueError(
                "meaning key must be String: {}".format(repr(mean))
            )

        self.mean = mean

    # magic methods  ===========================================================

    def __hash__(self):
        return hash(self.mean)

    def __eq__(self, other):
        # local import to avoid circular dependency with abbr_entry
        from kaye.prompt.abbr_collection.abbr_entry import AbbrEntry

        if not isinstance(other, AbbrEntry):
            return NotImplemented

        return self.mean == other.mean

    def __str__(self):
        return self.mean
