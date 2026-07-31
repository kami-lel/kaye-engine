"""
abbr_collection

define various data structures supporting **abbreviation nodes**
"""

from .abbr_tags import AbbrTags
from .abbr_wrap import AbbrWrap
from .abbr_data import AbbrData, get_abbr_data
from .abbr_data_loader import populate_abbr_data
from .abbr_meaning import AbbrMeaning
from .abbr_entry import AbbrEntry

__all__ = (
    "AbbrTags",
    "AbbrWrap",
    "AbbrData",
    "get_abbr_data",
    "populate_abbr_data",
    "AbbrMeaning",
    "AbbrEntry",
)
