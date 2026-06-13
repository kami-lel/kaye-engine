"""
s-exportable-abbrs_test.py

Unit tests for EXPORTABLE_ABBRS using SkillMDFileFrontmatterValidator.
"""

import pytest
from pydantic import ValidationError

from tests.cli.s import validate_abbr_group
from kaye.cli.exportable_abbr import EXPORTABLE_ABBRS

_g = {group.display_name: group for group in EXPORTABLE_ABBRS}

# valid – tag groups  ##########################################################


def test_abbr_programming_language_codes():
    r = validate_abbr_group(_g["Abbr Programming Language Codes"])
    assert r.name == "abbr-programming-language-codes"


def test_abbr_natural_language_codes():
    r = validate_abbr_group(_g["Abbr Natural Language Codes"])
    assert r.name == "abbr-natural-language-codes"


def test_abbr_units_of_measure():
    r = validate_abbr_group(_g["Abbr Units of Measure"])
    assert r.name == "abbr-units-of-measure"


def test_abbr_currency_symbols():
    r = validate_abbr_group(_g["Abbr Currency Symbols"])
    assert r.name == "abbr-currency-symbols"


def test_abbr_single_character():
    r = validate_abbr_group(_g["Abbr Single Character"])
    assert r.name == "abbr-single-character"


def test_abbr_emoji():
    r = validate_abbr_group(_g["Abbr Emoji"])
    assert r.name == "abbr-emoji"


# valid – wrap groups  #########################################################


def test_abbr_prefixes():
    r = validate_abbr_group(_g["Abbr Prefixes"])
    assert r.name == "abbr-prefixes"


def test_abbr_suffixes():
    r = validate_abbr_group(_g["Abbr Suffixes"])
    assert r.name == "abbr-suffixes"


def test_abbr_symbols():
    r = validate_abbr_group(_g["Abbr Symbols"])
    assert r.name == "abbr-symbols"


# valid – starts-with groups  ##################################################


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


def test_abbr_starts_with_k():
    r = validate_abbr_group(_g["Abbr Starts with K"])
    assert r.name == "abbr-starts-with-k"


def test_abbr_starts_with_l():
    r = validate_abbr_group(_g["Abbr Starts with L"])
    assert r.name == "abbr-starts-with-l"


def test_abbr_starts_with_m():
    r = validate_abbr_group(_g["Abbr Starts with M"])
    assert r.name == "abbr-starts-with-m"


def test_abbr_starts_with_n():
    r = validate_abbr_group(_g["Abbr Starts with N"])
    assert r.name == "abbr-starts-with-n"


def test_abbr_starts_with_o():
    r = validate_abbr_group(_g["Abbr Starts with O"])
    assert r.name == "abbr-starts-with-o"


def test_abbr_starts_with_p():
    r = validate_abbr_group(_g["Abbr Starts with P"])
    assert r.name == "abbr-starts-with-p"


def test_abbr_starts_with_q():
    r = validate_abbr_group(_g["Abbr Starts with Q"])
    assert r.name == "abbr-starts-with-q"


def test_abbr_starts_with_r():
    r = validate_abbr_group(_g["Abbr Starts with R"])
    assert r.name == "abbr-starts-with-r"


def test_abbr_starts_with_s():
    r = validate_abbr_group(_g["Abbr Starts with S"])
    assert r.name == "abbr-starts-with-s"


def test_abbr_starts_with_t():
    r = validate_abbr_group(_g["Abbr Starts with T"])
    assert r.name == "abbr-starts-with-t"


def test_abbr_starts_with_u():
    r = validate_abbr_group(_g["Abbr Starts with U"])
    assert r.name == "abbr-starts-with-u"


def test_abbr_starts_with_v():
    r = validate_abbr_group(_g["Abbr Starts with V"])
    assert r.name == "abbr-starts-with-v"


def test_abbr_starts_with_w():
    r = validate_abbr_group(_g["Abbr Starts with W"])
    assert r.name == "abbr-starts-with-w"


def test_abbr_starts_with_x():
    r = validate_abbr_group(_g["Abbr Starts with X"])
    assert r.name == "abbr-starts-with-x"


def test_abbr_starts_with_y():
    r = validate_abbr_group(_g["Abbr Starts with Y"])
    assert r.name == "abbr-starts-with-y"


def test_abbr_starts_with_z():
    r = validate_abbr_group(_g["Abbr Starts with Z"])
    assert r.name == "abbr-starts-with-z"


def test_abbr_starts_with_non_alphanumeric():
    r = validate_abbr_group(_g["Abbr Starts with Non-Alphanumeric"])
    assert r.name == "abbr-starts-with-non-alphanumeric"


# invalid – name pattern violation  ############################################


def test_abbr_starts_with_digits():
    with pytest.raises(ValidationError):
        validate_abbr_group(_g["Abbr Starts with Digits 0~9"])
