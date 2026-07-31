"""
abbr_data_loader.py

define ``populate_abbr_data`` -- parse already-loaded ``abbrs.json`` content
into an :class:`AbbrData` instance
"""

from .abbr_meaning import AbbrMeaning

__all__ = ("populate_abbr_data",)

# abbrs.json key constants
ABBRS_JSON_ABBRS_KEY = "abbrs"
ABBRS_JSON_REMARK_KEY = "remark"


# Public API  ##################################################################


def populate_abbr_data(data, abbrs_json):  # ===================================
    """
    walk already-loaded ``abbrs.json`` content and add each entry into
    ``data`` via :meth:`AbbrData.add_entry`

    should be called within a ``with data:`` block, so the automaton is
    rebuilt once on exit rather than left stale


    :param data: the instance to populate
    :type data: AbbrData
    :param abbrs_json: already-loaded ``abbrs.json`` content
    :type abbrs_json: dict
    :raises ValueError: malformed content, or an entry duplicating one
            already added
    """
    for mean_key, mean_obj in abbrs_json.items():
        if not isinstance(mean_obj, dict):
            raise ValueError(
                "meaning value must be Object: {}".format(repr(mean_obj))
            )

        if ABBRS_JSON_ABBRS_KEY not in mean_obj:
            raise ValueError(
                "meaning value must contains key: {}".format(
                    repr(ABBRS_JSON_ABBRS_KEY)
                )
            )

        remark = mean_obj.get(ABBRS_JSON_REMARK_KEY)
        mean = AbbrMeaning(mean_key, remark=remark)

        abbrs_obj = mean_obj[ABBRS_JSON_ABBRS_KEY]
        if not isinstance(abbrs_obj, dict):
            raise ValueError(
                "abbrs value must be Object: {}".format(repr(abbrs_obj))
            )

        for abbr, abbr_obj in abbrs_obj.items():
            data.add_entry(mean, abbr, abbr_obj)
