"""
claude_surface.py

define ``ClaudeSurface`` -- a combinable set of Claude surfaces, and the
affordance names available on each, declared directly as constants from
``docs/claude-doc.md``'s four availability tables (kept entirely separate
from ``affordance_registry``, a generic data structure with no surface
knowledge of its own).
"""

import enum

__all__ = ("ClaudeSurface",)


# constants  ###################################################################

_CHAT_AFFORDANCES = (
    "ClaudeChat:ask_user_input_v0",
    "ClaudeChat:places_map_display_v0",
    "ClaudeChat:places_list_display_v0",
    "ClaudeChat:recipe_display_v0",
    "ClaudeChat:itinerary_display_v0",
    "ClaudeChat:step_card_display_v0",
    "ClaudeChat:options_card_display_v0",
    "ClaudeChat:comparison_card_display_v0",
    "ClaudeChat:featured_card_display_v0",
    "ClaudeChat:product_carousel_display_v0",
    "ClaudeChat:link_preview_display_v0",
    "ClaudeChat:visualize:show_widget",
    "ClaudeChat:memory_",
    "ClaudeChat:weather_fetch",
    "ClaudeChat:places_search",
    "ClaudeChat:message_compose_v1",
)


_COWORK_TIER_AFFORDANCES = (
    "ClaudeCode:AskUserQuestion",
    "ClaudeCode:Skill",
    "ClaudeCode:Agent",
    "ClaudeCode:TaskStop",
)

_CODE_TIER_AFFORDANCES = (
    "ClaudeCode:Artifact",
    "ClaudeCode:SendUserFile",
    "ClaudeCode:PushNotification",
    "ClaudeCode:NotebookEdit",
    "ClaudeCode:RemoteTrigger",
    "ClaudeCode:DesignSync",
    "ClaudeCode:ReportFindings",
    "ClaudeCode:Enter/ExitPlanMode",
    "ClaudeCode:Enter/ExitWorktree",
    "ClaudeCode:ScheduleWakeup",
    "ClaudeCode:CronCreate/Delete/List",
    "ClaudeCode:Monitor",
    "ClaudeCode:SendMessage",
    "ClaudeCode:TaskCreate",
    "ClaudeCode:TaskGet",
    "ClaudeCode:TaskList",
    "ClaudeCode:TaskOutput",
    "ClaudeCode:TaskUpdate",
)

_VSC_TIER_AFFORDANCES = (
    "ClaudeCode:ListAgents",
    "ClaudeCode:TodoWrite",
)

_COWORK_AFFORDANCES = _COWORK_TIER_AFFORDANCES

_CODE_AFFORDANCES = _COWORK_TIER_AFFORDANCES + _CODE_TIER_AFFORDANCES

_VSC_AFFORDANCES = (
    _COWORK_TIER_AFFORDANCES + _CODE_TIER_AFFORDANCES + _VSC_TIER_AFFORDANCES
)

_AFFORDANCES_BY_SURFACE = {
    "chat": _CHAT_AFFORDANCES,
    "cowork": _COWORK_AFFORDANCES,
    "code": _CODE_AFFORDANCES,
    "vsc": _VSC_AFFORDANCES,
}


# Main Entry Point  ############################################################
class ClaudeSurface(enum.Flag):
    """
    a combinable set of Claude surfaces (``chat``, ``cowork``, ``code``,
    ``vsc``) -- resolves a requested surface combination into the
    affordance names to checkmark via ``render_prompt_lines``'s
    ``affordances=``/``contains_sidecars=`` kwargs
    """

    # fixme affordances are modeled as independent
    # per-surface membership, but some may actually be connected --
    # today `as_affordances()` and `as_contained_sidecars()` derive
    # from the identical per-surface data with no way to express
    # that a canonical name only does something under
    # `contains_sidecars` when the corpus also authored a bare node
    # for it (most don't, and there's no check that one exists).

    # pylint: disable=invalid-name
    chat = enum.auto()
    cowork = enum.auto()
    code = enum.auto()
    vsc = enum.auto()

    def as_affordances(self):
        """
        :return: canonical names of every affordance available on a
                surface set in ``self``, de-duplicated
        :rtype: tuple[str, ...]
        """
        names = set()
        for member in ClaudeSurface:
            if member in self:
                names.update(_AFFORDANCES_BY_SURFACE[member.name])
        return tuple(names)

    def as_contained_sidecars(self):
        """
        :return: ``as_affordances()``'s names, each bracket-wrapped, for
                the ``contains_sidecars=`` kwarg
        :rtype: tuple[str, ...]
        """
        return tuple("[{}]".format(name) for name in self.as_affordances())

    @classmethod
    def combine(cls, names):
        """
        :param names: member names to OR together (e.g. parsed
                ``--surface`` argv)
        :type names: Iterable[str]
        :return: the combined ``ClaudeSurface`` value
        :rtype: ClaudeSurface
        :example:
        >>> ClaudeSurface.combine(["chat", "cowork"])
        <ClaudeSurface.chat|cowork: 3>
        """
        combined = cls(0)
        for name in names:
            combined |= cls[name]
        return combined
