"""
abbr_data_loader.py

define ``load_abbr_data`` and ``get_abbr_data`` -- a single cached
``AbbrData`` instance, loaded once from an explicit ``file_path``
"""

import json

from .abbr_data import AbbrData

__all__ = (
    "load_abbr_data",
    "get_abbr_data",
)


# single cached AbbrData instance
_abbr_data = None


# Public API  ##################################################################


def load_abbr_data(file_path):  # ==============================================
    """
    parse ``file_path`` into an :class:`AbbrData` instance and cache it as
    the single abbr database


    :param file_path: path of the ``abbrs.json`` file to load
    :type file_path: Path or str
    :raises ValueError: an abbr database is already loaded
    :raises json.JSONDecodeError:
    :return: the loaded, cached :class:`AbbrData` instance
    :rtype: AbbrData
    """
    global _abbr_data  # pylint: disable=global-statement

    if _abbr_data is not None:
        raise ValueError("abbr data is already loaded")

    with open(file_path, "r", encoding="utf-8") as file:  # read only
        try:
            json_data = json.load(file)
        except json.JSONDecodeError as err:
            raise json.JSONDecodeError(
                "fail to parse abbrs.json: " + err.msg, err.doc, err.pos
            ) from err

    _abbr_data = AbbrData(abbrs_json_override=json_data)
    return _abbr_data


def get_abbr_data():  # ========================================================
    """
    :raises ValueError: no abbr data has been loaded yet via
            :func:`load_abbr_data`
    :return: the cached :class:`AbbrData` instance
    :rtype: AbbrData
    """
    if _abbr_data is None:
        raise ValueError("no abbr data loaded; call load_abbr_data() first")

    return _abbr_data
