"""
prompt-builtin_render_profiles_test.py

Unit Tests (using pytest) for:

- the built-in chat / cowork / code / vsc / ioschat profiles
- the built-in continue, hermes and comfy profiles
- AFFORDANCE_GROUPS
- BUILTIN_AFFORDANCES remarks
- register_builtin_render_profiles()
"""

import pytest

from kaye_engine.prompt.affordance_registry import (
    affordance_registry,
    variant_registry,
)
from kaye_engine.prompt.blueprint.render_profile_registry import (
    render_profile_registry,
)
from kaye_engine.prompt.builtin_affordances import (
    AFFORDANCE_GROUPS,
    BUILTIN_AFFORDANCES,
)
from kaye_engine.prompt.builtin_render_profiles import (
    register_builtin_render_profiles,
)
from tests.consumer_helper import isolated_render_profiles

_IDENTITY_NAMES = (
    "Claude",
    "ClaudeChat",
    "ClaudeCowork",
    "ClaudeCode",
    "ClaudeVSC",
    "ClaudeiOSChat",
)


def _profile(name):
    return render_profile_registry[name].profile


CHAT_PROFILE = _profile("chat")
COWORK_PROFILE = _profile("cowork")
CODE_PROFILE = _profile("code")
VSC_PROFILE = _profile("vsc")
IOSCHAT_PROFILE = _profile("ioschat")
CONTINUE_PROFILE = _profile("continue")
HERMES_PROFILE = _profile("hermes")
COMFY_PROFILE = _profile("comfy")


# Pytest unit tests  ###########################################################
class TestAffordances:

    def test_single_surface(_):
        assert "Claude:Skill" in COWORK_PROFILE.variants
        assert "Claude:weather_fetch" not in COWORK_PROFILE.variants

    def test_combined_surfaces(_):
        result = CODE_PROFILE.merge(VSC_PROFILE).variants

        assert "Claude:ReportFindings" in result
        assert "Claude:TodoWrite" in result

    def test_deduplicates_when_available_on_two_requested_surfaces(_):
        result = CODE_PROFILE.merge(VSC_PROFILE).variants

        assert result.count("Claude:Skill") == 1

    @pytest.mark.parametrize(
        "profile",
        [
            CHAT_PROFILE,
            COWORK_PROFILE,
            CODE_PROFILE,
            VSC_PROFILE,
            IOSCHAT_PROFILE,
        ],
    )
    def test_git_and_image_model_on_every_claude_surface(_, profile):
        assert "git" in profile.variants
        assert "QwenImage" in profile.variants

    def test_powershell_present_on_code_absent_on_vsc(_):
        assert "Claude:PowerShell" in CODE_PROFILE.variants
        assert "Claude:PowerShell" not in VSC_PROFILE.variants

    def test_web_bundle_on_every_surface(_):
        for profile in (
            CHAT_PROFILE,
            COWORK_PROFILE,
            CODE_PROFILE,
            VSC_PROFILE,
        ):
            assert "Claude:Web~" in profile.variants

    def test_agent_bundle_present_only_on_vsc(_):
        assert "Claude:Agent~" in VSC_PROFILE.variants
        assert "Claude:Agent~" not in CODE_PROFILE.variants
        assert "Claude:Agent~" not in COWORK_PROFILE.variants
        assert "Claude:Agent~" not in CHAT_PROFILE.variants

    def test_ioschat_calendar_variants_present_only_on_ioschat(_):
        for name in (
            "Claude:iOS:Calendar:EventEdit",
            "Claude:iOS:Calendar:EventInfo",
            "Claude:iOS:Calendar:Subcalendar",
        ):
            assert name in IOSCHAT_PROFILE.variants
            assert name not in CHAT_PROFILE.variants
            assert name not in COWORK_PROFILE.variants
            assert name not in CODE_PROFILE.variants
            assert name not in VSC_PROFILE.variants

    def test_ioschat_carries_every_chat_variant_too(_):
        for name in CHAT_PROFILE.variants:
            assert name in IOSCHAT_PROFILE.variants


class TestIdentityNamesAreNotVariants:

    def test_identity_names_absent_from_every_surfaces_variants(_):
        for name in _IDENTITY_NAMES:
            for entry in render_profile_registry.values():
                assert name not in entry.profile.variants

    def test_identity_names_absent_after_merge(_):
        combined = CODE_PROFILE.merge(VSC_PROFILE)

        assert "ClaudeCode" not in combined.variants
        assert "ClaudeVSC" not in combined.variants


class TestConditionalSidecars:

    def test_bracket_wraps_affordance_names(_):
        assert "[Claude:Skill]" in COWORK_PROFILE.conditional_sidecars

    def test_universal_identity_present_for_any_single_surface(_):
        assert "[Claude]" in CHAT_PROFILE.conditional_sidecars
        assert "[Claude]" in VSC_PROFILE.conditional_sidecars

    def test_single_surface_includes_own_identity_name_only(_):
        sidecars = CODE_PROFILE.conditional_sidecars

        assert "[ClaudeCode]" in sidecars
        assert "[ClaudeChat]" not in sidecars

    def test_combined_surfaces_include_each_identity_name(_):
        sidecars = CODE_PROFILE.merge(CHAT_PROFILE).conditional_sidecars

        assert "[ClaudeCode]" in sidecars
        assert "[ClaudeChat]" in sidecars

    def test_identity_names_do_not_collide_with_tool_affordance_names(_):
        sidecars = COWORK_PROFILE.conditional_sidecars

        assert "[Claude:Skill]" in sidecars
        assert sidecars.count("[ClaudeCowork]") == 1

    def test_vsc_has_no_identity_sidecar_of_its_siblings(_):
        sidecars = VSC_PROFILE.conditional_sidecars

        assert "[ClaudeChat]" not in sidecars
        assert "[ClaudeCowork]" not in sidecars
        assert "[ClaudeCode]" not in sidecars

    def test_claude_vsc_present_only_on_vsc(_):
        assert "[ClaudeVSC]" in VSC_PROFILE.conditional_sidecars
        assert "[ClaudeVSC]" not in CODE_PROFILE.conditional_sidecars
        assert "[ClaudeVSC]" not in COWORK_PROFILE.conditional_sidecars
        assert "[ClaudeVSC]" not in CHAT_PROFILE.conditional_sidecars

    def test_claude_vsc_survives_merge(_):
        combined = CODE_PROFILE.merge(VSC_PROFILE)

        assert "[ClaudeVSC]" in combined.conditional_sidecars

    def test_avoid_sidecar_on_every_profile(_):
        for entry in render_profile_registry.values():
            assert "avoid" in entry.profile.conditional_sidecars


class TestRegistry:

    def test_every_built_in_name_present_in_order(_):
        assert list(render_profile_registry)[:8] == [
            "chat",
            "cowork",
            "code",
            "vsc",
            "ioschat",
            "continue",
            "hermes",
            "comfy",
        ]

    def test_remarks(_):
        assert {
            name: entry.remark
            for name, entry in render_profile_registry.items()
        } == {
            "chat": "Anthropic Claude chat app on web and desktop",
            "cowork": "Anthropic Claude Cowork desktop agent",
            "code": "Anthropic Claude Code in the terminal",
            "vsc": "Anthropic Claude Code extension for Microsoft Visual"
            " Studio Code",
            "ioschat": "Anthropic Claude chat app on Apple iOS",
            "continue": "Continue.dev rules",
            "hermes": "Hermes Agents",
            "comfy": "Comfy Org ComfyUI image prompts",
        }

    def test_img_name_is_gone(_):
        assert "img" not in render_profile_registry

    def test_every_profile_variant_is_a_registered_variant(_):
        for entry in render_profile_registry.values():
            for name in entry.profile.variants or ():
                assert name in variant_registry, (entry.name, name)

    def test_repeated_call_is_idempotent(_):
        before = dict(render_profile_registry)
        register_builtin_render_profiles()
        assert render_profile_registry == before

    def test_registers_into_an_empty_registry(_):
        with isolated_render_profiles():
            register_builtin_render_profiles()
            assert len(render_profile_registry) == 8


class TestAffordanceGroups:

    def test_every_variant_registered(_):
        for affordance_name, variant_names in AFFORDANCE_GROUPS.items():
            for name in variant_names:
                assert variant_registry[name].affordance_name == (
                    affordance_name
                )

    def test_cli_registers_all_variants(_):
        assert set(AFFORDANCE_GROUPS["cli"]) == {
            "Claude:Bash",
            "Claude:PowerShell",
            "Claude:bash_tool",
            "Claude:Terminal~",
        }

    def test_ask_user_question_registers_both_variants(_):
        assert set(AFFORDANCE_GROUPS["ask-user-question"]) == {
            "Claude:ask_user_input_v0",
            "Claude:AskUserQuestion",
        }

    def test_web_registers_one_variant(_):
        assert set(AFFORDANCE_GROUPS["web"]) == {"Claude:Web~"}

    @pytest.mark.parametrize(
        "group, suffix",
        [
            ("calendar-event-edit", "EventEdit"),
            ("calendar-event-info", "EventInfo"),
            ("calendar-subcalendar", "Subcalendar"),
        ],
    )
    def test_calendar_groups_register_both_variants(_, group, suffix):
        variants = AFFORDANCE_GROUPS[group]

        assert len(variants) == 2
        assert all(name.endswith(suffix) for name in variants)

    def test_email_and_gtd_register_one_variant(_):
        assert set(AFFORDANCE_GROUPS["email-management"]) == {
            "Claude:Gmail",
        }
        assert set(AFFORDANCE_GROUPS["getting-things-done"]) == {
            "Claude:TickTick",
        }

    def test_image_model_registers_qwen_image(_):
        assert AFFORDANCE_GROUPS["image-model"] == ("QwenImage",)

    def test_identity_names_never_registered(_):
        for name in _IDENTITY_NAMES:
            assert name not in AFFORDANCE_GROUPS


class TestContentAndInteractionVariants:

    @pytest.mark.parametrize(
        "affordance, variant",
        [
            ("file-search", "Claude:FileSearch~"),
            ("skill", "Claude:~Skills"),
            ("tool", "Claude:ToolSearch"),
            ("push-notification", "Claude:Inbox~"),
            ("user-message", "Claude:SendUserMessage"),
            ("user-message", "Claude:ShowOnboardingRolePicker"),
            ("connector", "Claude:Connector~"),
            ("plugin", "Claude:Plugin~"),
            ("mcp-resource", "Claude:McpResource~"),
            ("doc", "Claude:Docs~"),
            ("pdf-viewer", "Claude:PDFViewer~"),
        ],
    )
    def test_variant_registered_under_affordance(_, affordance, variant):
        assert variant in AFFORDANCE_GROUPS[affordance]
        assert variant_registry[variant].affordance_name == affordance


class TestBrowserAndDeviceVariants:

    @pytest.mark.parametrize(
        "affordance, variant",
        [
            ("cli", "Claude:Terminal~"),
            ("browser", "Claude:Browser~"),
            ("browser", "Claude:Chrome~"),
            ("browser", "Claude:RemoteBrowser~"),
            ("computer-use", "Claude:ComputerUse~"),
            ("computer-use", "Claude:RemoteDevice~"),
            ("ide-diagnostics", "Claude:getDiagnostics"),
        ],
    )
    def test_variant_registered_under_affordance(_, affordance, variant):
        assert variant in AFFORDANCE_GROUPS[affordance]
        assert variant_registry[variant].affordance_name == affordance


class TestSessionAndSchedulingVariants:

    @pytest.mark.parametrize(
        "affordance, variant",
        [
            ("cron", "Claude:CodeRemote~"),
            ("cron", "Claude:ScheduledTasks~"),
            ("artifact", "Claude:RemoteArtifact~"),
            ("connector", "Claude:ccd_connectors~"),
            ("agent", "Claude:ccd_session~"),
            ("agent", "Claude:ccd_session_mgmt~"),
            ("app-management", "Claude:ccd_directory~"),
            ("app-management", "Claude:ccd_host~"),
            ("app-management", "Claude:ccd_pr~"),
            ("app-management", "Claude:ccd_settings~"),
            ("app-management", "Claude:ccd_sidebar~"),
            ("app-management", "Claude:ccd_turn~"),
            ("app-management", "Claude:ccd_view~"),
            ("app-management", "Claude:ccd_window~"),
            ("chat-utility", "Claude:claude_ai~"),
            ("chat-utility", "Claude:widgets~"),
        ],
    )
    def test_variant_registered_under_affordance(_, affordance, variant):
        assert variant in AFFORDANCE_GROUPS[affordance]
        assert variant_registry[variant].affordance_name == affordance


class TestBuiltinRemarks:

    def test_counts(_):
        assert len(BUILTIN_AFFORDANCES) == 54
        assert sum(len(v) for _, v in BUILTIN_AFFORDANCES.values()) == 84

    def test_affordance_groups_derived_from_data(_):
        assert AFFORDANCE_GROUPS == {
            name: tuple(variants)
            for name, (_, variants) in BUILTIN_AFFORDANCES.items()
        }

    def test_registered_remarks_match_data(_):
        for name, (remark, variants) in BUILTIN_AFFORDANCES.items():
            assert affordance_registry[name].remark == remark
            for variant_name, variant_remark in variants.items():
                assert variant_registry[variant_name].remark == variant_remark

    def test_every_remark_is_short_lowercase_text_without_period(_):
        remarks = []
        for remark, variants in BUILTIN_AFFORDANCES.values():
            remarks.append(remark)
            remarks.extend(variants.values())

        for remark in remarks:
            assert remark, remark
            assert remark[0].islower(), remark
            assert not remark.endswith("."), remark
            assert len(remark) <= 40, remark


class TestContinueProfile:

    def test_no_variants_but_gating_on(_):
        assert CONTINUE_PROFILE.variants == ()

    def test_only_avoid_sidecar(_):
        assert CONTINUE_PROFILE.conditional_sidecars == ("avoid",)

    def test_no_image_model(_):
        assert "QwenImage" not in CONTINUE_PROFILE.variants


class TestHermesProfile:

    def test_image_model_is_the_only_variant(_):
        assert HERMES_PROFILE.variants == ("QwenImage",)

    def test_image_model_identity_and_avoid_sidecars(_):
        assert HERMES_PROFILE.conditional_sidecars == (
            "[QwenImage]",
            "[for Hermes]",
            "avoid",
        )


class TestComfyProfile:

    def test_image_model_is_the_only_variant(_):
        assert COMFY_PROFILE.variants == ("QwenImage",)

    def test_no_file_edit_variant(_):
        for name in AFFORDANCE_GROUPS["file-edit"]:
            assert name not in COMFY_PROFILE.variants

    def test_no_claude_identity_sidecar(_):
        assert "[Claude]" not in COMFY_PROFILE.conditional_sidecars
        assert "avoid" in COMFY_PROFILE.conditional_sidecars
