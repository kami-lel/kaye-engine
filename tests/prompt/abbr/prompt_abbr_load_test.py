"""
prompt_abbr_load_test.py

Unit Tests (using pytest) for:

- load_abbrs_json()
"""

from pathlib import Path
import json

import pytest

from kaye.gen_prompt import DynamicAbbrBlueprint


class TestErr:  # err tests  ###################################################

    def test_bad_json(self):
        path = Path(__file__).resolve().parent / "malformated.json"
        with pytest.raises(json.JSONDecodeError) as exec_info:
            DynamicAbbrBlueprint.load_abbrs_json(
                abbrs_json_file_path_override=path
            )
        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "fail to parse abbrs.json: "
            "Expecting ',' delimiter: line 6 column 3 (char 105)"
        )
