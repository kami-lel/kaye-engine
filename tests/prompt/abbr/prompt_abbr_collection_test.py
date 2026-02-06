"""
prompt_abbr_collection_test.py

Unit Tests (using pytest) for: AbbrCollection
"""

# BUG

import pytest

from kaye.gen_prompt.abbr_collection import (
    AbbrEntry,
    AbbrWrap,
    AbbrTags,
    AbbrCollection,
)

# validation  ##################################################################
ABBR_OBJ_VALUE = {
    "mean": "for example",
    "tags": ["ascii", "usable"],
    "wrap": "word",
}
ALT_OBJ_VALUE = {
    "abbr": "e.g.",
    "tags": ["ascii"],
    "wrap": "prefix",
}


class TestValidate:

    def test_no_abbr(self):
        json_override = {
            "alt": {"ie": {"abbr": "i.e.", "tags": ["ascii"], "wrap": "word"}}
        }

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
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
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "abbrs.json must contains 'abbrs' and 'alt'"

    def test_bad_abbr(_):
        json_override = {"abbrs": "abc", "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "'abbrs' value must be object"

    def test_bad_alt(_):
        json_override = {"abbrs": {}, "alts": 5}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "'alts' value must be object"


class TestValidateAbbrs:

    def test_bad_key(_):
        json_override = {"abbrs": {5: {}}, "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "key must be string within 'abbrs' object: 5"

    def test_value_type(_):
        json_override = {"abbrs": {"eg": []}, "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "value must be object within 'abbrs' object: []"

    def test_mean_miss(_):
        entry_value = ABBR_OBJ_VALUE.copy()
        del entry_value["mean"]
        json_override = {"abbrs": {"e.g.": entry_value}, "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "abbrs object must contains mean"

    def test_mean_type(_):
        entry_value = ABBR_OBJ_VALUE.copy()
        entry_value["mean"] = 5
        json_override = {"abbrs": {"e.g.": entry_value}, "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "mean in abbrs object must be string: 5"

    def test_wrap_miss(_):
        entry_value = ABBR_OBJ_VALUE.copy()
        del entry_value["wrap"]
        json_override = {"abbrs": {"e.g.": entry_value}, "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "abbrs object must contains wrap"

    def test_wrap_type(_):
        entry_value = ABBR_OBJ_VALUE.copy()
        entry_value["wrap"] = 5
        json_override = {"abbrs": {"e.g.": entry_value}, "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "wrap in abbrs object must be string: 5"

    def test_tags_miss(_):
        entry_value = ABBR_OBJ_VALUE.copy()
        del entry_value["tags"]
        json_override = {"abbrs": {"e.g.": entry_value}, "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "abbrs object must contains tags"

    def test_tags_type(_):
        entry_value = ABBR_OBJ_VALUE.copy()
        entry_value["tags"] = "AAA"
        json_override = {"abbrs": {"e.g.": entry_value}, "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "tags in abbrs object must be array: 'AAA'"

    def test_tags_contains(_):
        entry_value = ABBR_OBJ_VALUE.copy()
        entry_value["tags"].append(5)
        json_override = {"abbrs": {"e.g.": entry_value}, "alts": {}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "tags in abbrs object must contains only string: "
            "['ascii', 'usable', 5]"
        )


class TestValidateAlts:

    def test_bad_key(_):
        json_override = {"abbrs": {}, "alts": {5: {}}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "key must be string within 'alts' object: 5"

    def test_value_type(_):
        json_override = {"abbrs": {}, "alts": {"eg": "some text"}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "value must be object within 'alts' object: 'some text'"

    def test_abbr_miss(_):
        entry_value = ALT_OBJ_VALUE.copy()
        del entry_value["abbr"]
        json_override = {"abbrs": {}, "alts": {"eg": entry_value}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "alts object must contains abbr"

    def test_abbr_type(_):
        entry_value = ALT_OBJ_VALUE.copy()
        entry_value["abbr"] = 5
        json_override = {"abbrs": {}, "alts": {"eg": entry_value}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "abbr in alts object must be string: 5"

    def test_wrap_miss(_):
        entry_value = ALT_OBJ_VALUE.copy()
        del entry_value["wrap"]
        json_override = {"abbrs": {}, "alts": {"eg": entry_value}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "alts object must contains wrap"

    def test_wrap_type(_):
        entry_value = ALT_OBJ_VALUE.copy()
        entry_value["wrap"] = 5
        json_override = {"abbrs": {}, "alts": {"eg": entry_value}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "wrap in alts object must be string: 5"

    def test_tags_miss(_):
        entry_value = ALT_OBJ_VALUE.copy()
        del entry_value["tags"]
        json_override = {"abbrs": {}, "alts": {"eg": entry_value}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "alts object must contains tags"

    def test_tags_type(_):
        entry_value = ALT_OBJ_VALUE.copy()
        entry_value["tags"] = "AAA"
        json_override = {"abbrs": {}, "alts": {"eg": entry_value}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert opt == "tags in alts object must be array: 'AAA'"

    def test_tags_contains(_):
        entry_value = ALT_OBJ_VALUE.copy()
        entry_value["tags"].append(5)
        json_override = {"abbrs": {}, "alts": {"eg": entry_value}}

        with pytest.raises(ValueError) as exec_info:
            AbbrCollection(abbrs_json_override=json_override)
        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt == "tags in alts object must contains only string: ['ascii', 5]"
        )


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
            "alts": {"eg": {"abbr": "e.g.", "tags": ["ascii"], "wrap": "word"}},
        }

        instance = AbbrCollection(abbrs_json_override=json_override)
        opt = instance.entries

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
