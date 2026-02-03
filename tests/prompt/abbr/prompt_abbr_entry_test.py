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
# TODO TODO


class TestFromAbbrErr:

    def test_no_mean1(_):
        abbr_obj = ABBR_OBJ.copy()
        del abbr_obj["mean"]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry.parse_from_abbr(KEY, abbr_obj)
        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "abbr_obj missing key 'mean': "
            "{'wrap': 'word', 'tags': ['ascii', 'usable']}"
        )

    def test_no_wrap1(_):
        abbr_obj = ABBR_OBJ.copy()
        del abbr_obj["wrap"]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry.parse_from_abbr(KEY, abbr_obj)
        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "abbr_obj missing key 'wrap': "
            "{'mean': 'average', 'tags': ['ascii', 'usable']}"
        )

    def test_no_tags1(_):
        abbr_obj = ABBR_OBJ.copy()
        del abbr_obj["tags"]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry.parse_from_abbr(KEY, abbr_obj)
        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "abbr_obj missing key 'tags': "
            "{'mean': 'average', 'wrap': 'word'}"
        )


# .parse_from_alt()  ###########################################################


# ._init__()  ##################################################################
class TestInitErr:

    def test_key1(_):
        key = 1

        with pytest.raises(TypeError) as exec_info:
            AbbrEntry(key, MEAN, WRAP, TAGS)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "arg key must be str: 1"

    def test_mean1(_):
        mean = 123

        with pytest.raises(TypeError) as exec_info:
            AbbrEntry(KEY, mean, WRAP, TAGS)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "arg mean must be str: 123"

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
