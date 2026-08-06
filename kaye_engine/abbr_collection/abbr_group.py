"""
abbr_group.py

define ``ABBRS_JSON_GROUP_KEY`` and ``AbbrGroupIndex``
"""

# abbrs.json key constant  #####################################################

ABBRS_JSON_GROUP_KEY = "groups"


# AbbrGroupIndex  ###############################################################


class AbbrGroupIndex:
    """
    track which :class:`AbbrEntry` instances belong to which **group**

    a group is a free-form, consumer-defined string carried on
    ``AbbrEntry.groups`` -- unlike :class:`AbbrTags`, there is no fixed
    enum of legal group names; any string an entry declares becomes a
    known group the moment it is added
    """

    def __init__(self):
        self._by_group = {}

    # entry addition  ==========================================================

    def add_entry(self, entry):
        """
        index ``entry`` under every group name in ``entry.groups``

        :param entry: entry to index
        :type entry: AbbrEntry
        """
        for group in entry.groups:
            self._by_group.setdefault(group, []).append(entry)

    # lookups  ==================================================================

    @property
    def names(self):
        """
        :return: every group name currently in use
        :rtype: frozenset[str]
        """
        return frozenset(self._by_group)

    def entries_for(self, group_name):
        """
        :param group_name: group name to look up
        :type group_name: str
        :return: every entry belonging to ``group_name``, insertion order;
                empty when ``group_name`` is unknown
        :rtype: tuple[AbbrEntry, ...]
        """
        return tuple(self._by_group.get(group_name, ()))
