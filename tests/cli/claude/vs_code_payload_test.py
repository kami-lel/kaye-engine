"""
vs_code_payload_test.py

Unit Tests (using pytest) for:

generate_vs_code_payload, export_vs_code_extension (stage wiring)
"""

from unittest.mock import patch

from kaye_engine.cli.claude.vs_code import export, payload
from kaye_engine.cli.dry_run import (
    disable_dry_run,
    enable_dry_run,
    is_dry_run,
)


# auxiliaries  #################################################################
def _fake_marketplace(folder, *, render_profile=None):
    path = folder / ".claude-plugin" / "marketplace.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        '{"name": "%s", "plugins": [{"name": "p"}]}' % folder.name,
        encoding="utf-8",
    )
    return path


def _fake_prompt(path, *, use_coder=False, render_profile=None):
    path.write_text("prompt\n", encoding="utf-8")


def _patch_stage_1():
    return (
        patch.object(payload, "export_marketplace", _fake_marketplace),
        patch.object(payload, "export_user_system_prompt_file", _fake_prompt),
        patch.object(payload, "get_marketplace_folder_name", lambda: "mk"),
    )


# pytest  ######################################################################
class TestGenerateVsCodePayload:

    def test_fills_any_folder_with_prompt_and_marketplace(_, tmp_path):
        a, b, c = _patch_stage_1()
        with a, b, c:
            path = payload.generate_vs_code_payload(tmp_path)

        assert (tmp_path / "CLAUDE.md").read_text(
            encoding="utf-8"
        ) == "prompt\n"
        assert path == tmp_path / "mk" / ".claude-plugin" / "marketplace.json"
        assert path.is_file()

    def test_places_nothing_outside_the_folder(_, tmp_path):
        target = tmp_path / "payload"
        target.mkdir()
        a, b, c = _patch_stage_1()
        with a, b, c:
            payload.generate_vs_code_payload(target)

        assert sorted(p.name for p in tmp_path.iterdir()) == ["payload"]


class TestExportVsCodeExtension:

    def test_runs_stage_1_into_temp_then_stage_2(_, tmp_path):
        seen = {}

        def fake_stage_1(folder, *, render_profile=None):
            seen["payload"] = folder
            seen["live"] = not is_dry_run()

        def fake_stage_2(payload_folder, claude_folder):
            seen["placed"] = (payload_folder, claude_folder)
            return tmp_path / "m.json"

        with patch.object(
            export, "generate_vs_code_payload", fake_stage_1
        ), patch.object(export, "place_vs_code_payload", fake_stage_2):
            result = export.export_vs_code_extension(tmp_path)

        assert seen["placed"] == (seen["payload"], tmp_path)
        assert result == tmp_path / "m.json"

    def test_dry_run_still_renders_stage_1_live(_, tmp_path):
        seen = {}

        def fake_stage_1(folder, *, render_profile=None):
            seen["live"] = not is_dry_run()

        enable_dry_run()
        try:
            with patch.object(
                export, "generate_vs_code_payload", fake_stage_1
            ), patch.object(
                export, "place_vs_code_payload", lambda p, c: tmp_path
            ):
                export.export_vs_code_extension(tmp_path)
            assert is_dry_run()
        finally:
            disable_dry_run()

        assert seen["live"] is True
