"""
prompt_abbr_entry_test.py

Unit Tests (using pytest) for: AbbrEntry
"""

import pytest
from kaye.gen_prompt.dynamic_abbr_blueprint import AbbrEntry

# testees  #####################################################################
KEY = "avg"
MEAN = "average"
WRAP = "word"
TAGS = ["ascii", "usable"]
ABBR_OBJ = {"mean": MEAN, "wrap": WRAP, "tags": TAGS}


# .parse_from_abbr()  ##########################################################


class TestFromAbbrErr:

    def test1(_):
        # TODO TODO
        key = "avg"
        abbr_obj = {"": 1}

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry.parse_from_abbr(KEY, abbr_obj)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == ""


# .parse_from_alt()  ###########################################################


# ._init__()  ##################################################################
class TestInitErr:

    def test_key1(_):
        key = 1

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(key, MEAN, WRAP, TAGS)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "'AAA' is not a valid AbbrWrap"

    def test_mean1(_):
        mean = 123

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(KEY, mean, WRAP, TAGS)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "'AAA' is not a valid AbbrWrap"

    def test_wrap1(_):
        wrap = "AAA"

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(KEY, MEAN, wrap, TAGS)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "'AAA' is not a valid AbbrWrap"

    def test_tags1(_):
        tags = ["ascii", 5]

        with pytest.raises(TypeError) as exec_info:
            AbbrEntry(KEY, MEAN, WRAP, tags)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "arg tags_list must list of str: ['ascii', 5]"

    def test_tags2(_):
        tags = ["ascii", "AAA"]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(KEY, MEAN, WRAP, tags)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "fail to parse 'AAA' as an abbr tag"
