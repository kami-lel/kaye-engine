"""
abbr_data.py

define ``AbbrData``
"""

import json
from pathlib import Path

import ahocorasick

from kaye.abbr_collection.abbr_entry import AbbrEntry
from kaye.abbr_collection.abbr_meaning import AbbrMeaning

# constants  ###################################################################

# abbrs.json path
ABBRS_JSON_FILE_PATH = Path(__file__).resolve().parent.parent / "abbrs.json"


# abbrs.json key constants
ABBRS_JSON_ABBRS_KEY = "abbrs"
ABBRS_JSON_REMARK_KEY = "remark"


# AbbrData  ####################################################################


class AbbrData:
    """
    represents collections of all abbreviation read from ``abbrs.json`


    :example:
    >>> instance = AbbrData()
    """

    # singleton pattern  =======================================================

    def __init__(self, *, abbrs_json_override=None):
        # fixme optimize as singleton
        self._load_abbrs_json(abbrs_json_override=abbrs_json_override)

    # load from abbrs.json  ====================================================

    def _load_abbrs_json(self, *, abbrs_json_override=None):
        """
        load from ``abbrs.json`` to create

        - ``self.meanings``
        - ``self.abbrs``
        - ``self.automaton``


        :raises json.JSONDecodeError:
        :raises ValueError:
        """
        # pylint: disable=attribute-defined-outside-init

        if abbrs_json_override:
            json_data = abbrs_json_override

        else:
            # read abbrs.json  -------------------------------------------------
            with open(
                ABBRS_JSON_FILE_PATH, "r", encoding="utf-8"
            ) as f:  # read only
                try:
                    json_data = json.load(f)
                except json.JSONDecodeError as err:
                    raise json.JSONDecodeError(
                        "fail to parse abbrs.json: " + err.msg,
                        err.doc,
                        err.pos,
                    ) from err

        # fill .meanings & .abbrs  ---------------------------------------------
        self.meanings = []
        self.abbrs = []
        for mean_key, mean_obj in json_data.items():
            if not isinstance(mean_obj, dict):
                raise ValueError(
                    "meaning value must be Object: {}".format(repr(mean_obj))
                )

            if ABBRS_JSON_ABBRS_KEY not in mean_obj:
                raise ValueError(
                    "meaning value must contains key: {}".format(
                        repr(ABBRS_JSON_ABBRS_KEY)
                    )
                )

            remark = mean_obj.get(ABBRS_JSON_REMARK_KEY)

            mean = AbbrMeaning(mean_key, remark=remark)
            self.meanings.append(mean)

            abbrs_obj = mean_obj[ABBRS_JSON_ABBRS_KEY]
            if not isinstance(abbrs_obj, dict):
                raise ValueError(
                    "abbrs value must be Object: {}".format(repr(abbrs_obj))
                )

            for abbr, abbr_obj in abbrs_obj.items():
                self.abbrs.append(AbbrEntry(mean, abbr, abbr_obj))

        # create automaton  ----------------------------------------------------
        # todo abbr data: use pickle.loads/dumps to save a local automaton, with hash
        # pylint: disable=c-extension-no-member
        automaton_entires = {}
        for entry in self.abbrs:
            abbr_lower = entry.abbr.lower()
            if abbr_lower not in automaton_entires:
                automaton_entires[abbr_lower] = []
            automaton_entires[abbr_lower].append(entry)

        self.automaton = ahocorasick.Automaton()
        for k, v in automaton_entires.items():
            self.automaton.add_word(k, tuple(v))
        self.automaton.make_automaton()
