"""
prompt_abbr_data_test.py

Unit Tests (using pytest) for:

- AbbrData
"""

import pytest

from kaye.gen_prompt import AbbrData, AbbrTags
from kaye.gen_prompt.abbr_collection import AbbrMeaning, AbbrEntry, AbbrWrap


# data validate  ###############################################################
class TestValidate:

    def test_mean_value(_):
        json_override = {"for example": 5}

        with pytest.raises(ValueError) as exec_info:
            AbbrData(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "meaning value must be Object: 5"


# test functions  ##############################################################
class Test1:  # ================================================================

    data = AbbrData(
        abbrs_json_override={
            "for example,for instance": {
                "e.g.": {
                    "priority": 5,
                    "tags": ["ascii_only", "common"],
                    "wrap": "word",
                },
                "eg": {
                    "priority": 6,
                    "tags": ["letters_only"],
                    "wrap": "prefix",
                },
            },
        }
    )

    def test_meanings(self):
        meanings = self.data.meanings

        print(meanings)

        assert len(meanings) == 1
        meaning = meanings[0]
        assert isinstance(meaning, AbbrMeaning)
        assert isinstance(meaning.mean, str)
        assert meaning.mean == "for example,for instance"

    def test_abbrs(self):
        abbrs = self.data.abbrs
        meaning = self.data.meanings[0]

        print(abbrs)

        assert len(abbrs) == 2

        # e.g.
        entry = abbrs[0]
        assert isinstance(entry, AbbrEntry)
        assert isinstance(entry.abbr, str)
        assert entry.abbr == "e.g."
        assert isinstance(entry.mean, AbbrMeaning)
        assert entry.mean is meaning
        assert isinstance(entry.priority, int)
        assert entry.priority == 5
        assert isinstance(entry.tags, AbbrTags)
        assert entry.tags == AbbrTags.ascii_only | AbbrTags.common
        assert isinstance(entry.wrap, AbbrWrap)
        assert entry.wrap == AbbrWrap.WORD

        # eg
        entry = abbrs[1]
        assert isinstance(entry, AbbrEntry)
        assert isinstance(entry.abbr, str)
        assert entry.abbr == "eg"
        assert isinstance(entry.mean, AbbrMeaning)
        assert entry.mean is meaning
        assert isinstance(entry.priority, int)
        assert entry.priority == 6
        assert isinstance(entry.tags, AbbrTags)
        assert entry.tags == AbbrTags.letters_only
        assert isinstance(entry.wrap, AbbrWrap)
        assert entry.wrap == AbbrWrap.PREFIX

    # automaton  ---------------------------------------------------------------

    def test_automaton(self):
        automaton = self.data.automaton
        abbrs = self.data.abbrs

        assert automaton.get("e.g.") is abbrs[0]
        assert automaton.get("eg") is abbrs[1]

    def test_automaton_fx1(self):
        ipt = "We can say, e.g. ..."
        opts_i = [15]
        opts_e = ["e.g.:for example,for instance"]

        automaton = self.data.automaton
        for result, opt_i, opt_e in zip(
            automaton.iter_long(ipt), opts_i, opts_e
        ):
            print(result)
            i, e = result
            assert i == opt_i
            assert str(e) == opt_e


class Test2:  # ================================================================

    data = AbbrData(
        abbrs_json_override={
            "footnote": {
                "†": {"priority": 5, "tags": ["common"], "wrap": "symbol"},
                "‡": {"priority": 6, "tags": ["common"], "wrap": "symbol"},
            },
            "fraction five eighths": {
                "⅝": {"priority": 5, "tags": ["common"], "wrap": "symbol"}
            },
            "-er,-or": {
                ".r": {"priority": 5, "tags": ["ascii_only"], "wrap": "suffix"}
            },
            "then": {
                "T": {"priority": 5, "tags": ["letters_only"], "wrap": "word"}
            },
            "ante meridiem,before midday": {
                "a.m.": {"priority": 5, "tags": ["ascii_only"], "wrap": "word"},
                "AM": {"priority": 6, "tags": ["letters_only"], "wrap": "word"},
            },
        }
    )

    def test_meanings(self):
        meanings = self.data.meanings

        print(meanings)

        assert len(meanings) == 5
        # footnote
        meaning = meanings[0]
        assert isinstance(meaning, AbbrMeaning)
        assert str(meaning) == "footnote"
        # 5/8
        meaning = meanings[1]
        assert isinstance(meaning, AbbrMeaning)
        assert str(meaning) == "fraction five eighths"
        # er
        meaning = meanings[2]
        assert isinstance(meaning, AbbrMeaning)
        assert str(meaning) == "-er,-or"
        # then
        meaning = meanings[3]
        assert isinstance(meaning, AbbrMeaning)
        assert str(meaning) == "then"
        # Am
        meaning = meanings[4]
        assert isinstance(meaning, AbbrMeaning)
        assert str(meaning) == "ante meridiem,before midday"

    # abbrs  -------------------------------------------------------------------
    def test_abbr_size(self):
        abbrs = self.data.abbrs

        print(abbrs)

        assert len(abbrs) == 7

    def test_abbrs1(self):
        abbrs = self.data.abbrs
        meaning = self.data.meanings[0]

        print(abbrs)

        entry = abbrs[0]
        assert isinstance(entry, AbbrEntry)
        assert entry.abbr == "†"
        assert entry.mean is meaning
        assert entry.priority == 5
        assert entry.tags == AbbrTags.common
        assert entry.wrap == AbbrWrap.SYMBOL

        entry = abbrs[1]
        assert isinstance(entry, AbbrEntry)
        assert entry.abbr == "‡"
        assert entry.mean is meaning
        assert entry.priority == 6
        assert entry.tags == AbbrTags.common
        assert entry.wrap == AbbrWrap.SYMBOL

    def test_abbrs2(self):
        abbrs = self.data.abbrs
        meaning = self.data.meanings[1]

        entry = abbrs[2]
        assert isinstance(entry, AbbrEntry)
        assert entry.abbr == "⅝"
        assert entry.mean is meaning
        assert entry.priority == 5
        assert entry.tags == AbbrTags.common
        assert entry.wrap == AbbrWrap.SYMBOL

    def test_abbrs3(self):
        abbrs = self.data.abbrs
        meaning = self.data.meanings[2]

        entry = abbrs[3]
        assert isinstance(entry, AbbrEntry)
        assert entry.abbr == ".r"
        assert entry.mean is meaning
        assert entry.priority == 5
        assert entry.tags == AbbrTags.ascii_only
        assert entry.wrap == AbbrWrap.SUFFIX

    def test_abbrs4(self):
        abbrs = self.data.abbrs
        meaning = self.data.meanings[3]

        entry = abbrs[4]
        assert isinstance(entry, AbbrEntry)
        assert entry.abbr == "T"
        assert entry.mean is meaning
        assert entry.priority == 5
        assert entry.tags == AbbrTags.letters_only
        assert entry.wrap == AbbrWrap.WORD

    def test_abbrs5(self):
        abbrs = self.data.abbrs
        meaning = self.data.meanings[4]

        entry = abbrs[5]
        assert isinstance(entry, AbbrEntry)
        assert entry.abbr == "a.m."
        assert entry.mean is meaning
        assert entry.priority == 5
        assert entry.tags == AbbrTags.ascii_only
        assert entry.wrap == AbbrWrap.WORD

        entry = abbrs[6]
        assert isinstance(entry, AbbrEntry)
        assert entry.abbr == "AM"
        assert entry.mean is meaning
        assert entry.priority == 6
        assert entry.tags == AbbrTags.letters_only
        assert entry.wrap == AbbrWrap.WORD

    # automaton  ---------------------------------------------------------------

    def test_automaton_fx1(self):  # HACK
        ipt = "Good mor.r but AM"
        opts_i = [9, 16]
        opts_e = [".r:-er,-or", "AM:ante meridiem,before midday"]

        automaton = self.data.automaton
        for result, opt_i, opt_e in zip(
            automaton.iter_long(ipt), opts_i, opts_e
        ):
            print(result)
            i, e = result
            assert i == opt_i
            assert str(e) == opt_e


# TODO TODO add more test cases with duplicated abbr
