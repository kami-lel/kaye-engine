"""
cli-s-structure-exportable_abbrs_test.py

Representative unit tests for EXPORTABLE_ABBRS using SkillMDFileFrontmatterValidator.
"""

import pytest
from pydantic import ValidationError

from tests.cli.s.u.structure import validate_abbr_group
from kaye.cli.exportable_abbr import EXPORTABLE_ABBRS

_g = {group.display_name: group for group in EXPORTABLE_ABBRS}


def test_abbr_programming_language_codes():
    r = validate_abbr_group(_g["Abbr Programming Language Codes"])
    assert r.name == "abbr-programming-language-codes"


def test_abbr_starts_with_a():
    r = validate_abbr_group(_g["Abbr Starts with A"])
    assert r.name == "abbr-starts-with-a"


def test_abbr_starts_with_b():
    r = validate_abbr_group(_g["Abbr Starts with B"])
    assert r.name == "abbr-starts-with-b"


def test_abbr_starts_with_c():
    r = validate_abbr_group(_g["Abbr Starts with C"])
    assert r.name == "abbr-starts-with-c"


def test_abbr_starts_with_d():
    r = validate_abbr_group(_g["Abbr Starts with D"])
    assert r.name == "abbr-starts-with-d"


def test_abbr_starts_with_e():
    r = validate_abbr_group(_g["Abbr Starts with E"])
    assert r.name == "abbr-starts-with-e"


def test_abbr_starts_with_f():
    r = validate_abbr_group(_g["Abbr Starts with F"])
    assert r.name == "abbr-starts-with-f"


def test_abbr_starts_with_g():
    r = validate_abbr_group(_g["Abbr Starts with G"])
    assert r.name == "abbr-starts-with-g"


def test_abbr_starts_with_h():
    r = validate_abbr_group(_g["Abbr Starts with H"])
    assert r.name == "abbr-starts-with-h"


def test_abbr_starts_with_i():
    r = validate_abbr_group(_g["Abbr Starts with I"])
    assert r.name == "abbr-starts-with-i"


def test_abbr_starts_with_j():
    r = validate_abbr_group(_g["Abbr Starts with J"])
    assert r.name == "abbr-starts-with-j"


def test_abbr_starts_with_digits():
    with pytest.raises(ValidationError):
        validate_abbr_group(_g["Abbr Starts with Digits 0~9"])
