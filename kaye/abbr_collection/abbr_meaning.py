"""
abbr_meaning.py

define ``AbbrMeaning``
"""


class AbbrMeaning:
    """
    represent a single meaning (of possible different spellings)
    """

    __slots__ = ("mean", "remark")

    def __init__(self, mean, remark=None):
        if not isinstance(mean, str):
            raise ValueError(
                "meaning key must be String: {}".format(repr(mean))
            )
        self.mean = mean

        if remark is not None and not isinstance(remark, str):
            raise ValueError("remark must be String: {}".format(repr(remark)))
        self.remark = remark

    # magic methods  ===========================================================

    def __hash__(self):
        return hash(self.mean)

    def __eq__(self, other):
        if not isinstance(other, AbbrMeaning):
            return NotImplemented

        return self.mean == other.mean

    def __str__(self):
        return self.mean
