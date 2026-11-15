"""
vs_code_place_test.py

Unit Tests (using pytest) for:

place_vs_code_payload
"""

import json

import pytest

from kaye_engine.cli.claude.vs_code.place import place_vs_code_payload
from kaye_engine.cli.dry_run import disable_dry_run, enable_dry_run

NAME = "mk"


# auxiliaries  #################################################################
@pytest.fixture(autouse=True)
def _live():
    disable_dry_run()
    yield
    disable_dry_run()


def _payload(root, *, prompt="prompt\n", plugins=("pa", "pb"), skill="s"):
    market = root / NAME
    (market / ".claude-plugin").mkdir(parents=True)
    (market / ".claude-plugin" / "marketplace.json").write_text(
        json.dumps({"name": NAME, "plugins": [{"name": p} for p in plugins]}),
        encoding="utf-8",
    )
    skill_file = market / "plugins" / "pa" / "skills" / "x" / "SKILL.md"
    skill_file.parent.mkdir(parents=True)
    skill_file.write_text(skill, encoding="utf-8")
    (root / "CLAUDE.md").write_text(prompt, encoding="utf-8")
    return root


@pytest.fixture
def payload(tmp_path):
    return _payload(tmp_path / "payload")


@pytest.fixture
def claude(tmp_path):
    return tmp_path / "claude"


def _settings(claude):
    return json.loads((claude / "settings.json").read_text(encoding="utf-8"))


def _baks(claude):
    return sorted(claude.glob("CLAUDE.md.*.bak"))


# pytest  ######################################################################
class TestFreshInstall:

    def test_creates_prompt_marketplace_and_settings(_, payload, claude):
        path = place_vs_code_payload(payload, claude)

        assert (claude / "CLAUDE.md").read_text(encoding="utf-8") == "prompt\n"
        assert path == claude / NAME / ".claude-plugin" / "marketplace.json"
        assert path.is_file()
        assert _baks(claude) == []

    def test_settings_registers_marketplace_and_enables_plugins(
        _, payload, claude
    ):
        place_vs_code_payload(payload, claude)

        assert _settings(claude) == {
            "extraKnownMarketplaces": {
                NAME: {
                    "source": {
                        "source": "directory",
                        "path": str((claude / NAME).resolve()),
                    }
                }
            },
            "enabledPlugins": {"pa@mk": True, "pb@mk": True},
        }

    def test_leaves_no_temp_name_behind(_, payload, claude):
        place_vs_code_payload(payload, claude)
        place_vs_code_payload(payload, claude)

        assert sorted(p.name for p in claude.iterdir()) == [
            "CLAUDE.md",
            NAME,
            "settings.json",
        ]


class TestClaudeMd:

    def test_differing_file_is_backed_up_then_replaced(_, payload, claude):
        claude.mkdir()
        (claude / "CLAUDE.md").write_text("old", encoding="utf-8")

        place_vs_code_payload(payload, claude)

        assert (claude / "CLAUDE.md").read_text(encoding="utf-8") == "prompt\n"
        baks = _baks(claude)
        assert len(baks) == 1
        assert baks[0].read_text(encoding="utf-8") == "old"

    def test_identical_file_is_left_alone(_, payload, claude):
        place_vs_code_payload(payload, claude)
        place_vs_code_payload(payload, claude)

        assert _baks(claude) == []

    def test_each_change_adds_a_backup_keeps_older(_, tmp_path, claude):
        place_vs_code_payload(_payload(tmp_path / "a", prompt="1"), claude)
        place_vs_code_payload(_payload(tmp_path / "b", prompt="2"), claude)
        place_vs_code_payload(_payload(tmp_path / "c", prompt="3"), claude)

        assert sorted(b.read_text(encoding="utf-8") for b in _baks(claude)) == [
            "1",
            "2",
        ]


class TestMarketplace:

    def test_changed_payload_swaps_the_folder(_, tmp_path, claude):
        place_vs_code_payload(_payload(tmp_path / "a", skill="old"), claude)
        place_vs_code_payload(_payload(tmp_path / "b", skill="new"), claude)

        skill = claude / NAME / "plugins" / "pa" / "skills" / "x" / "SKILL.md"
        assert skill.read_text(encoding="utf-8") == "new"

    def test_swap_drops_a_file_the_new_payload_lacks(_, tmp_path, claude):
        place_vs_code_payload(_payload(tmp_path / "a"), claude)
        stale = claude / NAME / "stale.txt"
        stale.write_text("x", encoding="utf-8")

        place_vs_code_payload(_payload(tmp_path / "b", skill="new"), claude)

        assert not stale.exists()

    def test_identical_tree_is_not_rewritten(_, payload, claude):
        place_vs_code_payload(payload, claude)
        marker = claude / NAME / "marker"
        marker.write_text("x", encoding="utf-8")
        (payload / NAME / "marker").write_text("x", encoding="utf-8")

        place_vs_code_payload(payload, claude)

        assert marker.exists()


class TestSettings:

    def test_other_keys_are_untouched(_, payload, claude):
        claude.mkdir()
        (claude / "settings.json").write_text(
            json.dumps({"theme": "dark", "enabledPlugins": {"x@y": True}}),
            encoding="utf-8",
        )

        place_vs_code_payload(payload, claude)

        settings = _settings(claude)
        assert settings["theme"] == "dark"
        assert settings["enabledPlugins"]["x@y"] is True
        assert settings["enabledPlugins"]["pa@mk"] is True
        assert list(settings)[:2] == ["theme", "enabledPlugins"]

    def test_existing_false_stays_false(_, payload, claude):
        claude.mkdir()
        (claude / "settings.json").write_text(
            json.dumps({"enabledPlugins": {"pa@mk": False}}), encoding="utf-8"
        )

        place_vs_code_payload(payload, claude)

        assert _settings(claude)["enabledPlugins"] == {
            "pa@mk": False,
            "pb@mk": True,
        }

    def test_existing_marketplace_entry_is_kept(_, payload, claude):
        claude.mkdir()
        other = {"source": {"source": "directory", "path": "/elsewhere"}}
        (claude / "settings.json").write_text(
            json.dumps({"extraKnownMarketplaces": {NAME: other}}),
            encoding="utf-8",
        )

        place_vs_code_payload(payload, claude)

        assert _settings(claude)["extraKnownMarketplaces"][NAME] == other

    def test_unchanged_settings_are_not_rewritten(_, payload, claude):
        place_vs_code_payload(payload, claude)
        text = (claude / "settings.json").read_text(encoding="utf-8")
        (claude / "settings.json").write_text(
            text.replace("  ", "    "), encoding="utf-8"
        )

        place_vs_code_payload(payload, claude)

        assert (claude / "settings.json").read_text(
            encoding="utf-8"
        ) == text.replace("  ", "    ")

    def test_invalid_json_aborts_with_nothing_written(_, payload, claude):
        claude.mkdir()
        (claude / "settings.json").write_text("{not json", encoding="utf-8")

        with pytest.raises(SystemExit) as info:
            place_vs_code_payload(payload, claude)

        assert info.value.code == 1
        assert (claude / "settings.json").read_text(
            encoding="utf-8"
        ) == "{not json"
        assert sorted(p.name for p in claude.iterdir()) == ["settings.json"]

    def test_wrong_key_type_aborts_with_nothing_written(_, payload, claude):
        claude.mkdir()
        (claude / "settings.json").write_text(
            '{"enabledPlugins": []}', encoding="utf-8"
        )

        with pytest.raises(SystemExit):
            place_vs_code_payload(payload, claude)

        assert sorted(p.name for p in claude.iterdir()) == ["settings.json"]


class TestIdempotence:

    def test_second_run_changes_nothing(_, payload, claude):
        place_vs_code_payload(payload, claude)
        before = {
            p: p.read_bytes() for p in claude.rglob("*") if p.is_file()
        }

        place_vs_code_payload(payload, claude)

        after = {p: p.read_bytes() for p in claude.rglob("*") if p.is_file()}
        assert after == before


class TestPreflight:

    def test_no_marketplace_folder_fails(_, tmp_path, claude):
        (tmp_path / "empty").mkdir()
        (tmp_path / "empty" / "CLAUDE.md").write_text("x", encoding="utf-8")

        with pytest.raises(SystemExit):
            place_vs_code_payload(tmp_path / "empty", claude)

        assert not claude.exists()

    def test_missing_claude_md_fails(_, payload, claude):
        (payload / "CLAUDE.md").unlink()

        with pytest.raises(SystemExit):
            place_vs_code_payload(payload, claude)

        assert not claude.exists()

    def test_name_differing_from_folder_fails(_, payload, claude):
        manifest = payload / NAME / ".claude-plugin" / "marketplace.json"
        manifest.write_text(
            json.dumps({"name": "other", "plugins": [{"name": "p"}]}),
            encoding="utf-8",
        )

        with pytest.raises(SystemExit):
            place_vs_code_payload(payload, claude)

    def test_no_plugins_fails(_, tmp_path, claude):
        with pytest.raises(SystemExit):
            place_vs_code_payload(
                _payload(tmp_path / "p", plugins=()), claude
            )

    def test_invalid_manifest_fails(_, payload, claude):
        (payload / NAME / ".claude-plugin" / "marketplace.json").write_text(
            "nope", encoding="utf-8"
        )

        with pytest.raises(SystemExit):
            place_vs_code_payload(payload, claude)

        assert not claude.exists()


class TestDryRun:

    def test_writes_nothing_under_a_missing_target(_, payload, claude):
        enable_dry_run()

        place_vs_code_payload(payload, claude)

        assert not claude.exists()

    def test_writes_nothing_over_an_existing_install(_, tmp_path, claude):
        place_vs_code_payload(_payload(tmp_path / "a", prompt="1"), claude)
        before = {p: p.read_bytes() for p in claude.rglob("*") if p.is_file()}

        enable_dry_run()
        place_vs_code_payload(
            _payload(tmp_path / "b", prompt="2", skill="new"), claude
        )

        after = {p: p.read_bytes() for p in claude.rglob("*") if p.is_file()}
        assert after == before
