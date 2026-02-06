"""
prompt_abbr_meaning_test.py

Unit Tests (using pytest) for:

- AbbrMeaning
"""

import pytest

from kaye.gen_prompt.abbr_collection import AbbrMeaning


class TestMeaning:

    def test1(_):
        mean = 5

        with pytest.raises(ValueError) as exec_info:
            AbbrMeaning(mean)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "meaning key must be String: 5"
