"""
abbr_collection

define various data structures supporting **abbreviation nodes**
"""

from .abbr_data import AbbrData, get_abbr_data
from .abbr_data_loader import populate_abbr_data_with_json_file
from .abbr_entry import AbbrEntry
from .abbr_glossary_registry import (
    AbbrGlossaryRegistry,
    abbr_glossary_registry,
    get_abbr_glossary,
    register_abbr_glossary,
)
from .abbr_meaning import AbbrMeaning
from .abbr_tags import AbbrTags
from .abbr_wrap import AbbrWrap

__all__ = (
    "AbbrData",
    "AbbrEntry",
    "AbbrGlossaryRegistry",
    "AbbrMeaning",
    "AbbrTags",
    "AbbrWrap",
    "abbr_glossary_registry",
    "get_abbr_data",
    "get_abbr_glossary",
    "populate_abbr_data_with_json_file",
    "register_abbr_glossary",
)
