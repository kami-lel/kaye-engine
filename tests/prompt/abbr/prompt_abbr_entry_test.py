"""
prompt_abbr_entry_test.py

Unit Tests (using pytest) for: AbbrEntry
"""

import pytest
from kaye.gen_prompt.dynamic_abbr_blueprint import AbbrEntry

# .parse_from_abbr  ############################################################


# .parse_from_alt()  ###########################################################


# ._init__()  ##################################################################
class TestInitErr:

    def test_wrap1(_):
        key = "avg"
        mean = "average"
        wrap = "AAA"
        tags = ["ascii"]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(key, mean, wrap, tags)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "'AAA' is not a valid AbbrWrap"

    def test_tags1(_):
        key = "avg"
        mean = "average"
        wrap = "word"
        tags = ["ascii", 5]

        with pytest.raises(TypeError) as exec_info:
            AbbrEntry(key, mean, wrap, tags)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "arg tags_list must list of str: ['ascii', 5]"

    def test_tags2(_):
        key = "avg"
        mean = "average"
        wrap = "word"
        tags = ["ascii", "AAA"]

        with pytest.raises(ValueError) as exec_info:
            AbbrEntry(key, mean, wrap, tags)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "fail to parse 'AAA' as an abbr tag"
