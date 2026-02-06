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


# BUG BUG
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


# automaton  ###################################################################

# TODO TODO
