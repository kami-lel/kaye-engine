"""
cli-s-structure-exportable_abbrs_test.py

Representative unit tests for EXPORTABLE_ABBRS using SkillMDFileFrontmatterValidator.
"""

import pytest
from pydantic import ValidationError

from tests.cli.s import validate_abbr_group
from kaye.cli.exportable_abbr import EXPORTABLE_ABBRS

_g = {group.display_name: group for group in EXPORTABLE_ABBRS}


def test_abbr_programming_language_codes():
    r = validate_abbr_group(_g["Abbr Programming Language Codes"])
    assert r.name == "abbr-programming-language-codes"


def test_abbr_starts_with_digits():
    with pytest.raises(ValidationError):
        validate_abbr_group(_g["Abbr Starts with Digits 0~9"])
