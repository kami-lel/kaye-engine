"""
prompt_abbr_entry_test.py

Unit Tests (using pytest) for: AbbrEntry
"""

import pytest
from kaye.gen_prompt.abbr_collection import (
    AbbrEntry,
    AbbrWrap,
    AbbrTags,
)

# testees  #####################################################################
ABBR_KEY = "e.g."
MEAN = "for example"
WRAP = "word"
ABBR_TAGS = ["ascii", "usable"]
ABBR_OBJ = {"mean": MEAN, "wrap": WRAP, "tags": ABBR_TAGS}
ALT_KEY = "eg"
ALT_OBJ = {"abbr": ABBR_KEY, "wrap": WRAP, "tags": ["ascii"]}
ABBRS_OBJ = {
    ABBR_KEY: ABBR_OBJ,
    "avg": {"mean": "average", "tags": ["ascii"], "wrap": "word"},
}


# .parse_from_alt()  ###########################################################
class TestFromAlt:

    def test1(_):
        opt = AbbrEntry.parse_from_alt(ALT_KEY, ALT_OBJ, ABBRS_OBJ)

        print(opt)
        assert isinstance(opt, AbbrEntry)

        assert isinstance(opt.key, str)
        assert opt.key == "eg"
        assert isinstance(opt.mean, str)
        assert opt.mean == "for example"
        assert isinstance(opt.wrap, AbbrWrap)
        assert opt.wrap == AbbrWrap.WORD
        assert isinstance(opt.tags, AbbrTags)
        assert opt.tags == AbbrTags.ascii


class TestFromAltErr:

    def test_no_abbr(_):
        abbrs_obj = ABBRS_OBJ.copy()
        del abbrs_obj["e.g."]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry.parse_from_alt(ALT_KEY, ALT_OBJ, abbrs_obj)
        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "fail to find referenced abbr 'e.g.' of alt 'eg' in abbrs.json"
        )

    def test_bad_init(_):
        alt_obj = ALT_OBJ.copy()
        alt_obj["wrap"] = 123

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry.parse_from_alt(ALT_KEY, alt_obj, ABBRS_OBJ)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "123 is not a valid AbbrWrap"


# ._init__()  ##################################################################
class TestInitErr:

    def test_key1(_):
        key = 1

        with pytest.raises(TypeError) as exec_info:
            AbbrEntry(key, MEAN, WRAP, ABBR_TAGS)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "arg key must be str: 1"

    def test_mean1(_):
        mean = 123

        with pytest.raises(TypeError) as exec_info:
            AbbrEntry(ABBR_KEY, mean, WRAP, ABBR_TAGS)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "arg mean must be str: 123"

    def test_wrap1(_):
        wrap = "AAA"

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(ABBR_KEY, MEAN, wrap, ABBR_TAGS)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "'AAA' is not a valid AbbrWrap"

    def test_tags2(_):
        tags = ["ascii", "AAA"]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(ABBR_KEY, MEAN, WRAP, tags)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "fail to parse 'AAA' as an abbr tag"


# .verify_found()  #############################################################
class TestVerify1:  # ==========================================================

    entry = AbbrEntry("my", "", "word", [])

    def test1(self):
        found = "my"
        wraps = ("", "")

        print(found, wraps, sep="\n")

        assert self.entry.verify_found(found, *wraps)

    def test2(self):
        found = "My"
        wraps = (" ", " ")

        print(found, wraps, sep="\n")

        assert self.entry.verify_found(found, *wraps)

    def test3(self):
        found = "MY"
        wraps = (" ", " ")

        print(found, wraps, sep="\n")

        assert self.entry.verify_found(found, *wraps)

    # false cases  *************************************************************
    def test_false1(self):
        found = "my"
        wraps = ("a", " ")

        print(found, wraps, sep="\n")

        assert not self.entry.verify_found(found, *wraps)

    def test_false2(self):
        found = "my"
        wraps = (" ", "b")

        print(found, wraps, sep="\n")

        assert not self.entry.verify_found(found, *wraps)


class TestVerify2:  # ==========================================================

    entry = AbbrEntry("My", "", "prefix", [])

    def test1(self):
        found = "My"
        wraps = (" ", "A")

        print(found, wraps, sep="\n")

        assert self.entry.verify_found(found, *wraps)

    # false cases  *************************************************************
    def test_false1(self):
        found = "my"
        wraps = (" ", "A")

        print(found, wraps, sep="\n")

        assert not self.entry.verify_found(found, *wraps)

    def test_false2(self):
        found = "MY"
        wraps = (" ", "A")

        print(found, wraps, sep="\n")

        assert not self.entry.verify_found(found, *wraps)


class TestVerify3:  # ==========================================================

    entry = AbbrEntry("My", "", "suffix", [])

    def test1(self):
        found = "My"
        wraps = ("A", " ")

        print(found, wraps, sep="\n")

        assert self.entry.verify_found(found, *wraps)

    # false cases  *************************************************************
    def test_false1(self):
        found = "my"
        wraps = ("A", " ")

        print(found, wraps, sep="\n")

        assert not self.entry.verify_found(found, *wraps)

    def test_false2(self):
        found = "MY"
        wraps = ("A", " ")

        print(found, wraps, sep="\n")

        assert not self.entry.verify_found(found, *wraps)


class TestVerify4:  # ==========================================================

    entry = AbbrEntry("=>", "", "symbol", [])

    def test1(self):
        found = "=>"
        wraps = ("A", " ")

        print(found, wraps, sep="\n")

        assert self.entry.verify_found(found, *wraps)
