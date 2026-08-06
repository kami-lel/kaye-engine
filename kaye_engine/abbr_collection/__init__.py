"""
abbr_collection

define various data structures supporting **abbreviation nodes**
"""

from .abbr_tags import AbbrTags
from .abbr_wrap import AbbrWrap
from .abbr_group import ABBRS_JSON_GROUP_KEY, AbbrGroupIndex
from .abbr_group_registry import (
    AbbrGroupRegistry,
    abbr_group_registry,
    register_abbr_group,
    get_abbr_group,
)
from .abbr_data import AbbrData, get_abbr_data
from .abbr_data_loader import populate_abbr_data_with_json_file
from .abbr_meaning import AbbrMeaning
from .abbr_entry import AbbrEntry

__all__ = (
    "AbbrTags",
    "AbbrWrap",
    "ABBRS_JSON_GROUP_KEY",
    "AbbrGroupIndex",
    "AbbrGroupRegistry",
    "abbr_group_registry",
    "register_abbr_group",
    "get_abbr_group",
    "AbbrData",
    "get_abbr_data",
    "populate_abbr_data_with_json_file",
    "AbbrMeaning",
    "AbbrEntry",
)
