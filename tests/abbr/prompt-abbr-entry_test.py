"""
prompt_abbr_entry_test.py

Unit Tests (using pytest) for: AbbrEntry
"""

import pytest
from kaye_engine.abbr_collection import (
    AbbrEntry,
    AbbrWrap,
    AbbrTags,
    AbbrMeaning,
)

MEAN = AbbrMeaning("for example")
ABBR = "e.g."
ABBR_OBJ = {"priority": 5, "tags": ["ascii_only", "common"], "wrap": "word"}
TERM_DEFINITION_OBJ = {"priority": 5, "tags": ["term_definition"], "wrap": "word"}


# err handling  ###############################################################


class TestErrAbbr:  # ==========================================================

    def test_key_type1(_):
        abbr = 5
        with pytest.raises(TypeError) as exec_info:
            AbbrEntry(MEAN, abbr, ABBR_OBJ)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "abbr key must be String: 5"


class TestErrAbbrObj:  # =======================================================

    def test_value_type1(_):
        abbr_obj = 5
        with pytest.raises(TypeError) as exec_info:
            AbbrEntry(MEAN, ABBR, abbr_obj)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "abbr value must be Object: 5"

    def test_missing_key1(_):
        abbr_obj = ABBR_OBJ.copy()
        del abbr_obj["priority"]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(MEAN, ABBR, abbr_obj)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "abbr value must contains key: ['priority']"

    def test_missing_key2(_):
        abbr_obj = ABBR_OBJ.copy()
        del abbr_obj["tags"]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(MEAN, ABBR, abbr_obj)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "abbr value must contains key: ['tags']"

    def test_missing_key3(_):
        abbr_obj = ABBR_OBJ.copy()
        del abbr_obj["priority"]
        del abbr_obj["wrap"]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(MEAN, ABBR, abbr_obj)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "abbr value must contains key: ['priority', 'wrap']"


class TestErrPriority:  # ======================================================

    def test_priority(_):
        abbr_obj = ABBR_OBJ.copy()
        abbr_obj["priority"] = "123"

        with pytest.raises(TypeError) as exec_info:
            AbbrEntry(MEAN, ABBR, abbr_obj)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "priority must be Integer: '123'"


class TestErrWrap:  # ==========================================================

    def test1(_):
        abbr_obj = ABBR_OBJ.copy()
        abbr_obj["wrap"] = 123

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(MEAN, ABBR, abbr_obj)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "123 is not a valid AbbrWrap"

    def test2(_):
        abbr_obj = ABBR_OBJ.copy()
        abbr_obj["wrap"] = "AAA"

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(MEAN, ABBR, abbr_obj)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "'AAA' is not a valid AbbrWrap"


class TestErrRemark:  # ========================================================

    def test1(_):
        abbr_obj = ABBR_OBJ.copy()
        abbr_obj["remark"] = 123

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(MEAN, ABBR, abbr_obj)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "remark must be String: 123"


class TestErrTags:  # ==========================================================

    def test_not_array(_):
        abbr_obj = ABBR_OBJ.copy()
        abbr_obj["tags"] = 123

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(MEAN, ABBR, abbr_obj)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "tags value must be Array: 123"

    def test_non_string_item(_):
        abbr_obj = ABBR_OBJ.copy()
        abbr_obj["tags"] = ["coding-terms", 5]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(MEAN, ABBR, abbr_obj)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "tags entry must be String: 5"


# init  ########################################################################
class TestInit:

    def test1(_):
        abbr_obj = {
            "priority": 0,
            "tags": [],
            "wrap": "word",
        }
        opt = AbbrEntry(AbbrMeaning("sometimes"), "s/X", abbr_obj)

        assert isinstance(opt.abbr, str)
        assert opt.abbr == "s/X"
        assert isinstance(opt.priority, int)
        assert opt.priority == 0
        assert isinstance(opt.mean, AbbrMeaning)
        assert opt.mean.mean == "sometimes"
        assert isinstance(opt.wrap, AbbrWrap)
        assert opt.wrap == AbbrWrap.WORD
        assert isinstance(opt.tags, AbbrTags)
        assert opt.tags == AbbrTags.NONE
        assert isinstance(opt.glossaries, tuple)
        assert opt.glossaries == ()
        assert opt.remark is None

    def test_remark(_):
        abbr_obj = {
            "priority": 0,
            "tags": [],
            "wrap": "word",
            "remark": "casual usage only",
        }
        opt = AbbrEntry(AbbrMeaning("sometimes"), "s/X", abbr_obj)

        assert opt.remark == "casual usage only"

    def test_glossaries(_):
        abbr_obj = {
            "priority": 0,
            "tags": ["coding-terms", "usable-abbreviations"],
            "wrap": "word",
        }
        opt = AbbrEntry(AbbrMeaning("sometimes"), "s/X", abbr_obj)

        assert opt.tags == AbbrTags.NONE
        assert opt.glossaries == ("coding-terms", "usable-abbreviations")

    def test_mixed_tags_and_glossaries(_):
        abbr_obj = {
            "priority": 0,
            "tags": ["single_character", "coding-terms"],
            "wrap": "word",
        }
        opt = AbbrEntry(AbbrMeaning("sometimes"), "s/X", abbr_obj)

        assert opt.tags == AbbrTags.single_character
        assert opt.glossaries == ("coding-terms",)


# .as_md_list_entry()  #########################################################
class TestAsMdListEntry:  # ====================================================

    def test_no_remark(_):
        entry = AbbrEntry(AbbrMeaning("for example"), "e.g.", ABBR_OBJ)
        assert entry.as_md_list_entry() == "- e.g.:for example"

    def test_mean_remark_only(_):
        mean = AbbrMeaning("for example", remark="Latin exempli gratia")
        entry = AbbrEntry(mean, "e.g.", ABBR_OBJ)
        assert entry.as_md_list_entry() == (
            "- e.g.:for example (Latin exempli gratia)"
        )

    def test_abbr_remark_only(_):
        abbr_obj = ABBR_OBJ.copy()
        abbr_obj["remark"] = "casual usage only"
        entry = AbbrEntry(AbbrMeaning("for example"), "e.g.", abbr_obj)
        assert entry.as_md_list_entry() == (
            "- e.g.:for example (casual usage only)"
        )

    def test_both_remarks(_):
        abbr_obj = ABBR_OBJ.copy()
        abbr_obj["remark"] = "casual usage only"
        mean = AbbrMeaning("for example", remark="Latin exempli gratia")
        entry = AbbrEntry(mean, "e.g.", abbr_obj)
        assert entry.as_md_list_entry() == (
            "- e.g.:for example (Latin exempli gratia; casual usage only)"
        )

    def test_number_no_remark(_):
        entry = AbbrEntry(AbbrMeaning("for example"), "e.g.", ABBR_OBJ)
        assert entry.as_md_list_entry(number=1) == "1. e.g.:for example"

    def test_number_with_remark(_):
        abbr_obj = ABBR_OBJ.copy()
        abbr_obj["remark"] = "casual usage only"
        entry = AbbrEntry(AbbrMeaning("for example"), "e.g.", abbr_obj)
        assert entry.as_md_list_entry(number=2) == (
            "2. e.g.:for example (casual usage only)"
        )

    def test_disable_remark_no_remark(_):
        entry = AbbrEntry(AbbrMeaning("for example"), "e.g.", ABBR_OBJ)
        assert entry.as_md_list_entry(is_remark_disabled=True) == (
            "- e.g.:for example"
        )

    def test_disable_remark_mean_remark_only(_):
        mean = AbbrMeaning("for example", remark="Latin exempli gratia")
        entry = AbbrEntry(mean, "e.g.", ABBR_OBJ)
        assert entry.as_md_list_entry(is_remark_disabled=True) == (
            "- e.g.:for example"
        )

    def test_disable_remark_abbr_remark_only(_):
        abbr_obj = ABBR_OBJ.copy()
        abbr_obj["remark"] = "casual usage only"
        entry = AbbrEntry(AbbrMeaning("for example"), "e.g.", abbr_obj)
        assert entry.as_md_list_entry(is_remark_disabled=True) == (
            "- e.g.:for example"
        )

    def test_disable_remark_both_remarks(_):
        abbr_obj = ABBR_OBJ.copy()
        abbr_obj["remark"] = "casual usage only"
        mean = AbbrMeaning("for example", remark="Latin exempli gratia")
        entry = AbbrEntry(mean, "e.g.", abbr_obj)
        assert entry.as_md_list_entry(is_remark_disabled=True) == (
            "- e.g.:for example"
        )


# .as_md_list_entry() w/ term_definition tag  ##################################
class TestAsMdListEntryTermDefinition:  # ======================================

    def test_no_remark(_):
        entry = AbbrEntry(AbbrMeaning("for example"), "e.g.", TERM_DEFINITION_OBJ)
        assert entry.as_md_list_entry() == "- for example"

    def test_mean_remark_only(_):
        mean = AbbrMeaning("for example", remark="Latin exempli gratia")
        entry = AbbrEntry(mean, "e.g.", TERM_DEFINITION_OBJ)
        assert entry.as_md_list_entry() == (
            "- for example (Latin exempli gratia)"
        )

    def test_abbr_remark_only(_):
        abbr_obj = TERM_DEFINITION_OBJ.copy()
        abbr_obj["remark"] = "casual usage only"
        entry = AbbrEntry(AbbrMeaning("for example"), "e.g.", abbr_obj)
        assert entry.as_md_list_entry() == (
            "- for example (casual usage only)"
        )

    def test_both_remarks(_):
        abbr_obj = TERM_DEFINITION_OBJ.copy()
        abbr_obj["remark"] = "casual usage only"
        mean = AbbrMeaning("for example", remark="Latin exempli gratia")
        entry = AbbrEntry(mean, "e.g.", abbr_obj)
        assert entry.as_md_list_entry() == (
            "- for example (Latin exempli gratia; casual usage only)"
        )

    def test_number_no_remark(_):
        entry = AbbrEntry(AbbrMeaning("for example"), "e.g.", TERM_DEFINITION_OBJ)
        assert entry.as_md_list_entry(number=1) == "1. for example"

    def test_disable_remark_with_remark(_):
        abbr_obj = TERM_DEFINITION_OBJ.copy()
        abbr_obj["remark"] = "casual usage only"
        entry = AbbrEntry(AbbrMeaning("for example"), "e.g.", abbr_obj)
        assert entry.as_md_list_entry(is_remark_disabled=True) == (
            "- for example"
        )


# .verify_found()  #############################################################
class TestVerify1:  # ==========================================================

    entry = AbbrEntry(MEAN, "my", {"priority": 0, "tags": [], "wrap": "word"})

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

    entry = AbbrEntry(MEAN, "My", {"priority": 0, "tags": [], "wrap": "prefix"})

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

    entry = AbbrEntry(MEAN, "My", {"priority": 0, "tags": [], "wrap": "suffix"})

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

    entry = AbbrEntry(MEAN, "=>", {"priority": 0, "tags": [], "wrap": "symbol"})

    def test1(self):
        found = "=>"
        wraps = (" ", " ")

        print(found, wraps, sep="\n")

        assert self.entry.verify_found(found, *wraps)

    # false cases  *************************************************************
    def test_false1(self):
        found = "=>"
        wraps = ("A", " ")

        print(found, wraps, sep="\n")

        assert not self.entry.verify_found(found, *wraps)


class TestVerifyTermDefinition:  # =============================================

    entry = AbbrEntry(MEAN, "e.g.", TERM_DEFINITION_OBJ)

    # false cases  *************************************************************
    def test_false1(self):
        found = "e.g."
        wraps = (" ", " ")  # satisfies the entry's own "word" wrap rule

        print(found, wraps, sep="\n")

        assert not self.entry.verify_found(found, *wraps)

    def test_false2(self):
        found = "e.g."
        wraps = ("", "")  # start/end of text, also satisfies "word"

        print(found, wraps, sep="\n")

        assert not self.entry.verify_found(found, *wraps)
