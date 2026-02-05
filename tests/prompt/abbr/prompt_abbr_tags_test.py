"""
prompt_abbr_tags_test.py

Unit Tests (using pytest) for: _AbbrTags
"""

import pytest
from kaye.gen_prompt.abbr_node import AbbrTags

# .parse test  #################################################################


class TestParseErr:

    def test_type1(_):
        ipt = [123, 456]

        with pytest.raises(ValueError) as exec_info:
            AbbrTags.parse(ipt)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "fail to parse 123 as an abbr tag"

    def test_type2(_):
        ipt = ["ascii", 5]

        with pytest.raises(ValueError) as exec_info:
            AbbrTags.parse(ipt)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "fail to parse 5 as an abbr tag"

    def test_value(_):
        ipt = ["abc"]

        with pytest.raises(ValueError) as exec_info:
            AbbrTags.parse(ipt)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "fail to parse 'abc' as an abbr tag"
