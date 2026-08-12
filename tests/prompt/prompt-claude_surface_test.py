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


class TestAsContainedSidecars:

    def test_bracket_wraps_affordance_names(_):
        sidecars = ClaudeSurface.cowork.as_contained_sidecars()

        assert "[ClaudeCode:Skill]" in sidecars


class TestCombine:

    def test_single_name(_):
        assert ClaudeSurface.combine(["chat"]) == ClaudeSurface.chat

    def test_multiple_names(_):
        combined = ClaudeSurface.combine(["chat", "cowork"])

        assert ClaudeSurface.chat in combined
        assert ClaudeSurface.cowork in combined
        assert ClaudeSurface.code not in combined
