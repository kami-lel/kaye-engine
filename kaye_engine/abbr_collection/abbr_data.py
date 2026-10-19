"""
abbr_data.py

define ``AbbrData``
"""

import ahocorasick

from kaye_engine.abbr_collection.abbr_entry import AbbrEntry
from kaye_engine.abbr_collection.abbr_glossary_registry import (
    abbr_glossary_registry,
)

# AbbrData  ####################################################################


class AbbrData:
    """
    holds collections of parsed abbreviation entries; starts empty and grows
    additively, one :class:`AbbrEntry` at a time, via :meth:`add_entry`,
    called within a ``with`` block

    one ``with`` block is one layer, e.g. one ``abbrs.json`` file; a later
    layer may repeat an (abbreviation, meaning) pair to add tags and
    glossaries to it, see :meth:`add_entry`


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
        self._entry_by_key = {}
        self._meaning_by_key = {}
        self._layer_entries = set()
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

        a pair (``abbr``, ``mean``) added by an earlier layer is merged
        instead of added: its tags and glossaries gain the new ones, a
        repeated tag or glossary is ignored, ``priority`` and ``wrap`` must
        match, and a ``remark`` missing at the meaning or entry level is
        filled in; the automaton is rebuilt on ``with`` block exit, not per
        call


        :param mean: the meaning this entry belongs to
        :type mean: AbbrMeaning
        :param abbr: the abbreviation text
        :type abbr: str
        :param abbr_obj: already-loaded ``abbrs.json`` entry content, see
                :class:`AbbrEntry`
        :type abbr_obj: dict
        :raises ValueError: malformed ``abbr_obj``, an entry duplicating one
                of the same layer, a repeat whose ``priority`` or ``wrap``
                differs, a ``remark`` conflicting at either level, or an
                entry referencing a glossary name never registered via
                ``register_abbr_glossary``
        """
        entry = AbbrEntry(mean, abbr, abbr_obj)
        if entry in self._layer_entries:
            raise ValueError("duplicate abbr entry: {}".format(repr(entry)))
        for glossary in entry.glossaries:
            if glossary not in abbr_glossary_registry:
                raise ValueError(
                    "unregistered abbr glossary: {}".format(repr(glossary))
                )

        entry.mean = self._merge_meaning(mean)
        self._layer_entries.add(entry)

        existing = self._entry_by_key.get(entry)
        if existing is not None:
            self._merge_entry(existing, entry)
            return

        self._entry_by_key[entry] = entry
        self.abbrs.append(entry)

    def _merge_meaning(self, mean):
        """
        :return: the tracked meaning equal to ``mean``, its missing remark
                filled from ``mean``; ``mean`` itself, now tracked, if new
        :rtype: AbbrMeaning
        :raises ValueError: both carry a remark, and they differ
        """
        tracked = self._meaning_by_key.get(mean.mean)
        if tracked is None:
            self._meaning_by_key[mean.mean] = mean
            self.meanings.append(mean)
            return mean

        tracked.remark = _merge_remark(tracked.remark, mean.remark, mean)
        return tracked

    @staticmethod
    def _merge_entry(existing, entry):
        """
        fold the repeated ``entry`` into ``existing``

        :raises ValueError: ``priority`` or ``wrap`` differ, or both carry
                a remark, and they differ
        """
        for field in ("priority", "wrap"):
            if getattr(existing, field) != getattr(entry, field):
                raise ValueError(
                    "repeated abbr entry {} changes {}: {} -> {}".format(
                        repr(entry),
                        field,
                        repr(getattr(existing, field)),
                        repr(getattr(entry, field)),
                    )
                )

        existing.remark = _merge_remark(existing.remark, entry.remark, entry)
        existing.tags |= entry.tags
        existing.glossaries = (
            *existing.glossaries,
            *(g for g in entry.glossaries if g not in existing.glossaries),
        )

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
        self._layer_entries = set()
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


def _merge_remark(old, new, owner):
    """
    :return: ``old``, or ``new`` when ``old`` is missing
    :rtype: str or None
    :raises ValueError: both are set, and they differ
    """
    if old is None:
        return new
    if new is not None and new != old:
        raise ValueError(
            "conflicting remark for {}: {} -> {}".format(
                repr(owner), repr(old), repr(new)
            )
        )
    return old


# single, always-present singleton instance  ###################################

_abbr_data = AbbrData()


def get_abbr_data():  # ========================================================
    """
    :return: the single, always-present :class:`AbbrData` singleton, which
            may still be empty; check via ``bool(get_abbr_data())``
    :rtype: AbbrData
    """
    return _abbr_data
