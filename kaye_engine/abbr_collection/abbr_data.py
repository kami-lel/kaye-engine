"""
abbr_data.py

define ``AbbrData``
"""

import ahocorasick

from kaye_engine.abbr_collection.abbr_entry import AbbrEntry
from kaye_engine.abbr_collection.abbr_meaning import AbbrMeaning

# constants  ###################################################################

# abbrs.json key constants
ABBRS_JSON_ABBRS_KEY = "abbrs"
ABBRS_JSON_REMARK_KEY = "remark"


# AbbrData  ####################################################################


class AbbrData:
    """
    represents collections of all abbreviation parsed from already-loaded
    ``abbrs.json`` content


    :example:
    >>> instance = AbbrData(abbrs_json_override=json_data)
    """

    def __init__(self, *, abbrs_json_override):
        """
        parse already-loaded ``abbrs.json`` content to create

        - ``self.meanings``
        - ``self.abbrs``
        - ``self.automaton``


        :raises ValueError:
        """
        # fill .meanings & .abbrs  ---------------------------------------------
        self.meanings = []
        self.abbrs = []
        for mean_key, mean_obj in abbrs_json_override.items():
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
        # fixme abbr data: use pickle.loads/dumps to save a local automaton, with hash
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
