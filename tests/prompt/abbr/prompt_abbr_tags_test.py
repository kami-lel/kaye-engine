"""
prompt_abbr_load_test.py

Unit Tests (using pytest) for: _AbbrTags
"""

from pathlib import Path
import json

import pytest

from kaye.gen_prompt import DynamicAbbrBlueprint

JSON_FILES_FOLDER = Path(__file__).resolve().parent


class TestErr:  # err tests  ###################################################

    def test_bad_json(self):
        path = JSON_FILES_FOLDER / "bad_parse.json"
        with pytest.raises(json.JSONDecodeError) as exec_info:
            DynamicAbbrBlueprint.load_abbrs_json(
                abbrs_json_file_path_override=path
            )
        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == "fail to parse abbrs.json: "
            "Expecting value: line 6 column 1 (char 46)"
        )

    def test_no_abbr(self):
        path = JSON_FILES_FOLDER / "bad_no_abbr.json"

        with pytest.raises(ValueError) as exec_info:
            DynamicAbbrBlueprint.load_abbrs_json(
                abbrs_json_file_path_override=path
            )
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "abbrs.json must contains 'abbrs' and 'alt'"

    def test_no_alt(self):
        path = JSON_FILES_FOLDER / "bad_no_alt.json"

        with pytest.raises(ValueError) as exec_info:
            DynamicAbbrBlueprint.load_abbrs_json(
                abbrs_json_file_path_override=path
            )
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "abbrs.json must contains 'abbrs' and 'alt'"
