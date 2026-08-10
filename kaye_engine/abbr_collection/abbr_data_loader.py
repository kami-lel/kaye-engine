"""
abbr_data_loader.py

define ``populate_abbr_data_with_json_file`` -- parse an ``abbrs.json``
file and add each entry into an :class:`AbbrData` instance
"""

import json

from .abbr_data import get_abbr_data
from .abbr_meaning import AbbrMeaning

__all__ = ("populate_abbr_data_with_json_file",)

# abbrs.json key constants
ABBRS_JSON_ABBRS_KEY = "abbrs"
ABBRS_JSON_REMARK_KEY = "remark"


# Public API  ##################################################################


def populate_abbr_data_with_json_file(file_path):  # ===========================
    """
    parse ``file_path`` and add each entry into the single
    :func:`get_abbr_data` instance via :meth:`AbbrData.add_entry`

    the automaton is rebuilt once, after the whole file has been applied;
    every exportable abbr group (tags, glossaries, wraps, first-char
    buckets) is then re-registered via
    :func:`kaye_engine.cli.exportable_abbr.register_exportable_abbrs`, so
    callers need not register those groups themselves


    :param file_path: path of the ``abbrs.json`` file to load
    :type file_path: Path or str
    :raises json.JSONDecodeError:
    :raises ValueError: malformed content, or an entry duplicating one
            already added
    """
    with open(file_path, "r", encoding="utf-8") as file:  # read only
        try:
            abbrs_json = json.load(file)
        except json.JSONDecodeError as err:
            raise json.JSONDecodeError(
                "fail to parse abbrs.json: " + err.msg, err.doc, err.pos
            ) from err

    data = get_abbr_data()
    with data:
        for mean_key, mean_obj in abbrs_json.items():
            if not isinstance(mean_obj, dict):
                raise TypeError(
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
                raise TypeError(
                    "abbrs value must be Object: {}".format(repr(abbrs_obj))
                )

            for abbr, abbr_obj in abbrs_obj.items():
                data.add_entry(mean, abbr, abbr_obj)

    # pylint: disable-next=import-outside-toplevel
    from kaye_engine.cli.exportable_abbr import register_exportable_abbrs

    register_exportable_abbrs()
