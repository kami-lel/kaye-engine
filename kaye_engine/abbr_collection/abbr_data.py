"""
abbr_data.py

define ``AbbrData``
"""

import ahocorasick

from kaye_engine.abbr_collection.abbr_entry import AbbrEntry

# AbbrData  ####################################################################


class AbbrData:
    """
    holds collections of parsed abbreviation entries; starts empty and grows
    additively, one :class:`AbbrEntry` at a time, via :meth:`add_entry`,
    called within a ``with`` block


    :example:
    >>> data = AbbrData()
    >>> with data:
    ...     mean = AbbrMeaning("for example", remark=None)
    ...     data.add_entry(mean, "e.g.", {"priority": 5, "tags": [], "wrap": "word"})
    """

    def __init__(self):
        """
        create an empty instance with

        - ``self.meanings``
        - ``self.abbrs``
        - ``self.automaton``
        """
        self.meanings = []
        self.abbrs = []
        self._seen_entries = set()
        self._editing = False

        self.automaton = (
            ahocorasick.Automaton()
        )  # pylint: disable=c-extension-no-member
        self.automaton.make_automaton()

    # entry addition  ==========================================================

    def add_entry(self, mean, abbr, abbr_obj):
        """
        add a single abbreviation entry, merging it into

        - ``self.meanings`` (``mean`` itself, if not already tracked)
        - ``self.abbrs``

        the automaton is rebuilt on ``with`` block exit, not per call


        :param mean: the meaning this entry belongs to
        :type mean: AbbrMeaning
        :param abbr: the abbreviation text
        :type abbr: str
        :param abbr_obj: already-loaded ``abbrs.json`` entry content, see
                :class:`AbbrEntry`
        :type abbr_obj: dict
        :raises ValueError: malformed ``abbr_obj``, or an entry duplicating
                one already added
        """
        entry = AbbrEntry(mean, abbr, abbr_obj)
        if entry in self._seen_entries:
            raise ValueError("duplicate abbr entry: {}".format(repr(entry)))
        self._seen_entries.add(entry)
        self.abbrs.append(entry)

        if mean not in self.meanings:
            self.meanings.append(mean)

    def _rebuild_automaton(self):
        # fixme fixme abbr data: use pickle.loads/dumps to save a local automaton, with hash
        # pylint: disable=c-extension-no-member
        automaton_entires = {}
        for entry in self.abbrs:
            abbr_lower = entry.abbr.lower()
            if abbr_lower not in automaton_entires:
                automaton_entires[abbr_lower] = []
            automaton_entires[abbr_lower].append(entry)

        automaton = ahocorasick.Automaton()
        for k, v in automaton_entires.items():
            automaton.add_word(k, tuple(v))
        automaton.make_automaton()
        self.automaton = automaton

    # support context manager  =================================================

    def __enter__(self):
        self._editing = True
        return self

    def __exit__(self, *args):
        self._editing = False
        if args[0] is None:
            self._rebuild_automaton()

    # magic method  ============================================================

    def __bool__(self):
        """
        :return: whether this instance holds at least one entry
        :rtype: bool
        """
        return bool(self.abbrs)


# single, always-present singleton instance  ###################################

_abbr_data = AbbrData()


def get_abbr_data():  # ========================================================
    """
    :return: the single, always-present :class:`AbbrData` singleton, empty
            if nothing has been added yet
    :rtype: AbbrData
    """
    # FIXME abbr data need to warn for empty abbrs
    return _abbr_data
