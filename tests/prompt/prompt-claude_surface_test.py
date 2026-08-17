"""
prompt-claude_surface_test.py

Unit Tests (using pytest) for:

- ClaudeSurface.as_affordances()
- ClaudeSurface.as_contained_sidecars()
- ClaudeSurface.combine()
"""

from kaye_engine.prompt.claude_surface import ClaudeSurface


# Pytest unit tests  ###########################################################
class TestAsAffordances:

    def test_single_member(_):
        assert "ClaudeCode:Skill" in ClaudeSurface.cowork.as_affordances()
        assert (
            "ClaudeChat:weather_fetch"
            not in ClaudeSurface.cowork.as_affordances()
        )

    def test_combined_members(_):
        combined = ClaudeSurface.code | ClaudeSurface.vsc
        result = combined.as_affordances()

        assert "ClaudeCode:ReportFindings" in result
        assert "ClaudeCode:TodoWrite" in result

    def test_deduplicates_when_available_on_two_requested_surfaces(_):
        combined = ClaudeSurface.code | ClaudeSurface.vsc
        result = combined.as_affordances()

        assert result.count("ClaudeCode:Skill") == 1

    def test_universal_affordance_present_for_any_single_surface(_):
        assert "Claude" in ClaudeSurface.chat.as_affordances()
        assert "Claude" in ClaudeSurface.vsc.as_affordances()

    def test_per_surface_identity_affordance_is_exclusive_to_own_member(_):
        assert "ClaudeCode" in ClaudeSurface.code.as_affordances()
        assert "ClaudeCode" not in ClaudeSurface.vsc.as_affordances()

    def test_vsc_has_no_identity_affordance_of_its_own(_):
        vsc_affordances = ClaudeSurface.vsc.as_affordances()

        assert "ClaudeChat" not in vsc_affordances
        assert "ClaudeCowork" not in vsc_affordances
        assert "ClaudeCode" not in vsc_affordances

    def test_git_present_only_on_vsc(_):
        assert "git" in ClaudeSurface.vsc.as_affordances()
        assert "git" not in ClaudeSurface.code.as_affordances()
        assert "git" not in ClaudeSurface.cowork.as_affordances()
        assert "git" not in ClaudeSurface.chat.as_affordances()


class TestAsContainedSidecars:

    def test_bracket_wraps_affordance_names(_):
        sidecars = ClaudeSurface.cowork.as_contained_sidecars()

        assert "[ClaudeCode:Skill]" in sidecars

    def test_single_surface_includes_own_identity_name_only(_):
        sidecars = ClaudeSurface.code.as_contained_sidecars()

        assert "[ClaudeCode]" in sidecars
        assert "[ClaudeChat]" not in sidecars

    def test_combined_surfaces_include_each_identity_name(_):
        combined = ClaudeSurface.code | ClaudeSurface.chat
        sidecars = combined.as_contained_sidecars()

        assert "[ClaudeCode]" in sidecars
        assert "[ClaudeChat]" in sidecars

    def test_identity_names_do_not_collide_with_tool_affordance_names(_):
        sidecars = ClaudeSurface.cowork.as_contained_sidecars()

        assert "[ClaudeCode:Skill]" in sidecars
        assert "[ClaudeCowork]" in sidecars
        assert sidecars.count("[ClaudeCowork]") == 1


class TestCombine:

    def test_single_name(_):
        assert ClaudeSurface.combine(["chat"]) == ClaudeSurface.chat

    def test_multiple_names(_):
        combined = ClaudeSurface.combine(["chat", "cowork"])

        assert ClaudeSurface.chat in combined
        assert ClaudeSurface.cowork in combined
        assert ClaudeSurface.code not in combined
