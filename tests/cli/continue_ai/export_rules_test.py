"""
export_rules_test.py

Unit Tests (using pytest) for:

- classify_exportable()
- export_continue_folder()
"""

from unittest.mock import MagicMock, patch

import pytest

from kaye_engine.cli.continue_ai.export_rules import (
    classify_exportable,
    export_continue_folder,
)
from kaye_engine.cli.exportable_abbr import ExportableAbbr
from kaye_engine.prompt.blueprint import BlueprintRegistry


def _registry(name, **kwargs):
    blueprint = MagicMock()
    blueprint.sidecars.description_and_when_to_use = "d"
    blueprint.sidecars.globs = []
    blueprint.render_prompt.return_value = "body of " + name
    return BlueprintRegistry(
        canonical_name=name,
        display_name="Display " + name,
        blueprint=blueprint,
        **kwargs,
    )


# pytest  ######################################################################
class TestClassifyExportable:

    def test_always_apply_beats_llm_invokable_false(_):
        reg = _registry("x", always_apply=True, llm_invokable=False)

        assert classify_exportable(reg) == "rule"

    def test_always_apply_beats_not_user_invokable(_):
        reg = _registry(
            "x",
            always_apply=True,
            llm_invokable=False,
            is_user_invokable=False,
        )

        assert classify_exportable(reg) == "rule"

    def test_llm_invokable_is_rule(_):
        assert classify_exportable(_registry("x")) == "rule"

    def test_user_invokable_only_is_prompt(_):
        reg = _registry("x", llm_invokable=False)

        assert classify_exportable(reg) == "prompt"

    def test_neither_invokable_is_skipped(_):
        reg = _registry("x", llm_invokable=False, is_user_invokable=False)

        assert classify_exportable(reg) is None

    def test_abbr_group_is_rule(_):
        group = ExportableAbbr(canonical_name="a", display_name="A")

        assert classify_exportable(group) == "rule"


class TestExportContinueFolder:

    @pytest.fixture
    def fake_registry(_):
        entries = {
            "r": _registry("r"),
            "always": _registry(
                "always", always_apply=True, llm_invokable=False
            ),
            "p": _registry("p", llm_invokable=False),
            "skip": _registry(
                "skip", llm_invokable=False, is_user_invokable=False
            ),
        }
        with patch(
            "kaye_engine.cli.continue_ai.export_rules.exportable_registry",
            entries,
        ):
            yield entries

    def test_writes_expected_files(_, tmp_path, fake_registry):
        export_continue_folder(tmp_path)

        rules = sorted(p.name for p in (tmp_path / "rules").iterdir())
        prompts = sorted(p.name for p in (tmp_path / "prompts").iterdir())
        assert rules == ["always.md", "r.md"]
        assert prompts == ["p.md"]

    def test_content(_, tmp_path, fake_registry):
        export_continue_folder(tmp_path)

        always = (tmp_path / "rules" / "always.md").read_text("utf-8")
        prompt = (tmp_path / "prompts" / "p.md").read_text("utf-8")
        assert "alwaysApply: true" in always
        assert "invokable: true" in prompt
        assert "alwaysApply: false" in prompt

    def test_creates_both_subfolders_even_if_empty(_, tmp_path):
        with patch(
            "kaye_engine.cli.continue_ai.export_rules.exportable_registry",
            {},
        ):
            export_continue_folder(tmp_path / "new")

        assert (tmp_path / "new" / "rules").is_dir()
        assert (tmp_path / "new" / "prompts").is_dir()

    def test_unwritable_destination_exits_1(_, tmp_path, fake_registry):
        blocker = tmp_path / "file"
        blocker.write_text("x")

        with pytest.raises(SystemExit) as exc_info:
            export_continue_folder(blocker)

        assert exc_info.value.code == 1

    def test_write_failure_exits_1(_, tmp_path, fake_registry):
        with patch(
            "kaye_engine.cli.continue_ai.export_rules.ContinueRule.write",
            side_effect=OSError("boom"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                export_continue_folder(tmp_path)

        assert exc_info.value.code == 1

    def test_forwards_render_profile(_, tmp_path, fake_registry):
        profile = MagicMock()
        with patch(
            "kaye_engine.cli.continue_ai.export_rules.ContinueRule"
        ) as rule_cls:
            export_continue_folder(tmp_path, render_profile=profile)

        for call in rule_cls.from_exportable.call_args_list:
            assert call.kwargs["render_profile"] is profile
