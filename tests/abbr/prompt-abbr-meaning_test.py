"""
prompt_abbr_meaning_test.py

Unit Tests (using pytest) for:

- AbbrMeaning
"""

import pytest

from kaye_engine.abbr_collection import AbbrMeaning


class TestMeaning:

    def test1(_):
        mean = 5

        with pytest.raises(ValueError) as exec_info:
            AbbrMeaning(mean)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "meaning key must be String: 5"


class TestRemark:

    def test_default_none(_):
        mean = AbbrMeaning("for example")
        assert mean.remark is None

    def test_set(_):
        mean = AbbrMeaning("for example", remark="Latin exempli gratia")
        assert mean.remark == "Latin exempli gratia"

    def test_invalid_type(_):
        with pytest.raises(ValueError) as exec_info:
            AbbrMeaning("for example", remark=5)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "remark must be String: 5"
