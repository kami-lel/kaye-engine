"""
prompt_abbr_load_test.py

Unit Tests (using pytest) for: load_abbrs_json()
"""

from pathlib import Path
import json

import pytest

from kaye.gen_prompt import DynamicAbbrBlueprint, AbbrEntry, AbbrWrap, AbbrTags

JSON_FILES_FOLDER = Path(__file__).resolve().parent / "json_testees"


# read file  ###################################################################
class TestFileErr:

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


# entries population  ##########################################################
class TestEntries:

    def test1(_):
        path = JSON_FILES_FOLDER / "entries.json"

        DynamicAbbrBlueprint._entries = None
        DynamicAbbrBlueprint.load_abbrs_json(
            abbrs_json_file_path_override=path
        )
        opt = DynamicAbbrBlueprint._entries

        assert isinstance(opt, list)
        assert len(opt) == 3
        # entry e.g.
        entry = opt[0]
        assert isinstance(entry, AbbrEntry)
        assert entry.key == "e.g."
        assert entry.mean == "for example,for instance"
        assert entry.wrap == AbbrWrap.WORD
        assert entry.tags == AbbrTags.ascii
        # entry eg
        entry = opt[1]
        assert isinstance(entry, AbbrEntry)
        assert entry.key == ".m"
        assert entry.mean == "-ism"
        assert entry.wrap == AbbrWrap.SUFFIX
        assert entry.tags == AbbrTags.ascii

        # entry avg
        entry = opt[2]
        assert isinstance(entry, AbbrEntry)
        assert entry.key == "eg"
        assert entry.mean == "for example,for instance"
        assert entry.wrap == AbbrWrap.WORD
        assert entry.tags == AbbrTags.ascii


# automation  ##################################################################
class TestAutomation:

    def test1(_):
        path = JSON_FILES_FOLDER / "entries.json"

        DynamicAbbrBlueprint._automaton = None
        DynamicAbbrBlueprint.load_abbrs_json(
            abbrs_json_file_path_override=path
        )
        opt = DynamicAbbrBlueprint._automaton

        print(opt)
        assert False  # HACK HACK
