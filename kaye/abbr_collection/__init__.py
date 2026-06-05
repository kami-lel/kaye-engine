"""
abbr_collection

define various data structures supporting **abbreviation nodes**
"""

from .abbr_tags import AbbrTags
from .abbr_wrap import AbbrWrap
from .abbr_data import AbbrData
from .abbr_meaning import AbbrMeaning
from .abbr_entry import AbbrEntry

__all__ = ("AbbrTags", "AbbrWrap", "AbbrData", "AbbrMeaning", "AbbrEntry")
