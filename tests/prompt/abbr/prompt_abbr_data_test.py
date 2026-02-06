"""
prompt_abbr_data_test.py

Unit Tests (using pytest) for:

- AbbrData
"""

import pytest

from kaye.gen_prompt import AbbrData

# data validate  ###############################################################


class TestValidate:

    def test_mean_value(_):
        json_override = {"for example": 5}

        with pytest.raises(ValueError) as exec_info:
            AbbrData(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "meaning value must be Object: 5"
