"""
abbr_data.py

define ``AbbrData``
"""

import json
from pathlib import Path

import ahocorasick

from kaye.abbr_collection.abbr_entry import AbbrEntry
from kaye.abbr_collection.abbr_meaning import AbbrMeaning

# abbrs.json path  #############################################################

ABBRS_JSON_FILE_PATH = Path(__file__).resolve().parent.parent / "abbrs.json"


# AbbrData  ####################################################################


class AbbrData:
    """
    represents collections of all abbreviation read from ``abbrs.json`


    :example:
    >>> instance = AbbrData()
    """

    # singleton pattern  =======================================================

    def __init__(self, *, abbrs_json_override=None):
        # Fixme optimize as singleton
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
            mean = AbbrMeaning(mean_key)
            self.meanings.append(mean)

            if not isinstance(mean_obj, dict):
                raise ValueError(
                    "meaning value must be Object: {}".format(repr(mean_obj))
                )

            for abbr, abbr_obj in mean_obj.items():
                self.abbrs.append(AbbrEntry(mean, abbr, abbr_obj))

        # create automaton  ----------------------------------------------------
        # todo use pickle.loads/dumps to save a local automaton, with hash
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
