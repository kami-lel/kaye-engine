"""
prompt_abbr_tags_test.py

Unit Tests (using pytest) for: _AbbrTags
"""

import pytest
from kaye.gen_prompt.dynamic_abbr_blueprint import AbbrTags

# .parse test  #################################################################


class TestParseErr:

    def test_type1(_):
        ipt = 123

        with pytest.raises(TypeError) as exec_info:
            AbbrTags.parse(ipt)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "arg tags_list must list of str: 123"

    def test_type2(_):
        ipt = [123, 456]

        with pytest.raises(TypeError) as exec_info:
            AbbrTags.parse(ipt)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "arg tags_list must list of str: [123, 456]"

    def test_value(_):
        ipt = ["abc"]

        with pytest.raises(ValueError) as exec_info:
            AbbrTags.parse(ipt)

        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "fail to parse 'abc' as an abbr tag"
