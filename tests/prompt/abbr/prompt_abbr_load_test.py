"""
prompt_abbr_load_test.py

Unit Tests (using pytest) for: load_abbrs_json()
"""

import pytest

from kaye.gen_prompt import AbbrNode, AbbrEntry, AbbrWrap, AbbrTags

# validation  ##################################################################


class TestValidate:

    def test_no_abbr(self):
        json_override = {
            "alt": {"ie": {"abbr": "i.e.", "tags": ["ascii"], "wrap": "word"}}
        }

        with pytest.raises(ValueError) as exec_info:
            AbbrNode.load_abbrs_json(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "abbrs.json must contains 'abbrs' and 'alt'"

    def test_no_alt(self):
        json_override = {
            "abbrs": {
                "i.e.": {
                    "mean": "that is,in other words",
                    "tags": ["ascii"],
                    "wrap": "word",
                }
            }
        }

        with pytest.raises(ValueError) as exec_info:
            AbbrNode.load_abbrs_json(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "abbrs.json must contains 'abbrs' and 'alt'"

    def test_bad_abbr(_):
        json_override = {"abbrs": "abc", "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrNode.load_abbrs_json(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "'abbrs' value must be object"

    def test_bad_alt(_):
        json_override = {"abbrs": {}, "alts": 5}

        with pytest.raises(ValueError) as exec_info:
            AbbrNode.load_abbrs_json(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "'alts' value must be object"


class TestValidateAbbrs:

    def test_bad_key(_):
        json_override = {"abbrs": {5: {}}, "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrNode.load_abbrs_json(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "key must be string within 'abbrs' object: 5"

    def test_value_type(_):
        json_override = {"abbrs": {"eg": []}, "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrNode.load_abbrs_json(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "value must be object within 'abbrs' object: []"

    # TODO TODO


class TestValidateAlts:

    def test_bad_key(_):
        json_override = {"abbrs": {}, "alts": {5: {}}}

        with pytest.raises(ValueError) as exec_info:
            AbbrNode.load_abbrs_json(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "key must be string within 'alts' object: 5"

    def test_value_type(_):
        json_override = {"abbrs": {}, "alts": {"eg": "some text"}}

        with pytest.raises(ValueError) as exec_info:
            AbbrNode.load_abbrs_json(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "value must be object within 'alts' object: 'some text'"

    # TODO TODO


# entries population  ##########################################################
class TestEntries:

    def test1(_):
        json_override = {
            "abbrs": {
                "e.g.": {
                    "mean": "for example,for instance",
                    "tags": ["ascii"],
                    "wrap": "word",
                },
                ".m": {"mean": "-ism", "tags": ["ascii"], "wrap": "suffix"},
            },
            "alts": {
                "eg": {"abbr": "e.g.", "tags": ["ascii"], "wrap": "word"}
            },
        }

        AbbrNode._entries = None
        AbbrNode.load_abbrs_json(abbrs_json_override=json_override)
        opt = AbbrNode._entries

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
