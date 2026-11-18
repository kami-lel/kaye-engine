"""
vs_code_place_test.py

Unit Tests (using pytest) for:

place_vs_code_payload
"""

import json
import logging

import kamilog
import pytest

from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
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


# log output  ##################################################################
def _lines(caplog):
    """:return: (level, badges, message) of every record, in order"""
    return [
        (r.levelno, getattr(r, "badges", ()), r.message)
        for r in caplog.records
    ]


def _messages(caplog, badge=None):
    return [
        m for _, badges, m in _lines(caplog) if badge is None or badge in badges
    ]


class TestLogOutput:

    @pytest.fixture(autouse=True)
    def _capture(_, caplog):
        caplog.set_level(logging.DEBUG, logger=LOGGER_CLAUDE_NAME)

    def test_phases_are_entered_in_order(_, payload, claude, caplog):
        place_vs_code_payload(payload, claude)

        entered = [
            m for lv, _b, m in _lines(caplog) if lv == kamilog.ENTER
        ]
        assert entered == [
            "preflight: check payload and settings, write nothing",
            "merge CLAUDE.md",
            "swap marketplace folder mk",
            "merge settings.json",
        ]

    def test_each_preflight_check_that_passes_is_logged(
        _, payload, claude, caplog
    ):
        place_vs_code_payload(payload, claude)

        passed = [m for m in _messages(caplog) if m.startswith("pass:")]
        assert len(passed) == 4
        assert all(
            lv == logging.DEBUG
            for lv, _b, m in _lines(caplog) if m.startswith("pass:")
        )

    def test_prompt_write_logs_tmp_then_mv_then_create(
        _, payload, claude, caplog
    ):
        place_vs_code_payload(payload, claude)

        steps = [
            (b, m.split()[0]) for _lv, b, m in _lines(caplog)
            if "CLAUDE.md" in m and not m.startswith(("merge", "pass"))
        ]
        assert steps == [
            (("tmp",), "create"), (("mv",), "move"), (("new",), "create"),
        ]

    def test_backup_is_a_cp_line(_, tmp_path, claude, caplog):
        place_vs_code_payload(_payload(tmp_path / "a", prompt="1"), claude)
        caplog.clear()

        place_vs_code_payload(_payload(tmp_path / "b", prompt="2"), claude)

        copies = _messages(caplog, "cp")
        assert len(copies) == 1
        assert copies[0].startswith("copy ") and ".bak" in copies[0]

    def test_marketplace_diff_lists_each_file_then_counts(
        _, tmp_path, claude, caplog
    ):
        place_vs_code_payload(_payload(tmp_path / "a", skill="1"), claude)
        extra = claude / NAME / "gone.txt"
        extra.write_text("x", encoding="utf-8")
        caplog.clear()

        place_vs_code_payload(_payload(tmp_path / "b", skill="2"), claude)

        assert _messages(caplog, "owr")[:1] == [
            "change plugins/pa/skills/x/SKILL.md"
        ]
        assert "remove gone.txt" in _messages(caplog, "del")
        assert "mk: 0 added, 1 changed, 1 removed" in _messages(caplog)

    def test_swap_steps_follow_the_algorithm(_, tmp_path, claude, caplog):
        place_vs_code_payload(_payload(tmp_path / "a", skill="1"), claude)
        caplog.clear()

        place_vs_code_payload(_payload(tmp_path / "b", skill="2"), claude)

        swap = [
            (b, m.split()[0]) for _lv, b, m in _lines(caplog)
            if ".new-" in m or ".old-" in m
        ]
        assert swap == [
            (("tmp",), "create"),
            (("mv",), "move"),
            (("mv",), "move"),
            (("del",), "delete"),
        ]

    def test_added_settings_keys_are_one_new_line_each(
        _, payload, claude, caplog
    ):
        place_vs_code_payload(payload, claude)

        assert [
            m for m in _messages(caplog, "new") if "settings.json" in m
        ] == [
            "add marketplace mk to settings.json",
            "add pa@mk to settings.json",
            "add pb@mk to settings.json",
        ]

    def test_kept_existing_key_is_a_skip_line(_, payload, claude, caplog):
        place_vs_code_payload(payload, claude)
        data = _settings(claude)
        data["enabledPlugins"]["pa@mk"] = False
        data["enabledPlugins"].pop("pb@mk")
        (claude / "settings.json").write_text(json.dumps(data), "utf-8")
        caplog.clear()

        place_vs_code_payload(payload, claude)

        skips = [m for lv, _b, m in _lines(caplog) if lv == kamilog.SKIP]
        assert "keep pa@mk: already False" in skips
        assert "add pb@mk to settings.json" in _messages(caplog, "new")

    def test_second_run_skips_every_target_and_writes_nothing(
        _, payload, claude, caplog
    ):
        place_vs_code_payload(payload, claude)
        caplog.clear()

        place_vs_code_payload(payload, claude)

        skips = [m for lv, _b, m in _lines(caplog) if lv == kamilog.SKIP]
        assert sum(m.startswith("unchanged") for m in skips) == 3
        for badge in ("tmp", "mv", "del", "new", "cp"):
            assert not _messages(caplog, badge)

    def test_dry_run_logs_the_same_lines_as_a_live_run(
        _, tmp_path, claude, caplog
    ):
        dry_claude = tmp_path / "dry-claude"
        enable_dry_run()
        place_vs_code_payload(_payload(tmp_path / "p"), dry_claude)
        dry = _lines(caplog)
        caplog.clear()
        disable_dry_run()

        place_vs_code_payload(_payload(tmp_path / "p2"), claude)
        live = _lines(caplog)

        assert not dry_claude.exists()

        def shape(lines):
            # the dry badge leads every dry line; everything else is equal
            return [
                (lv, tuple(x for x in b if x != "dry"), m.split()[0])
                for lv, b, m in lines
            ]

        assert shape(dry) == shape(live)

    def test_rollback_logs_undo_caution(
        _, tmp_path, claude, caplog, monkeypatch
    ):
        place_vs_code_payload(_payload(tmp_path / "a", skill="1"), claude)
        caplog.clear()
        real_replace = __import__("os").replace
        calls = {"n": 0}

        def fail_second(src, dst):
            calls["n"] += 1
            if calls["n"] == 2:  # the move of the new folder into place
                raise OSError("denied")
            return real_replace(src, dst)

        monkeypatch.setattr(
            "kaye_engine.cli.claude.vs_code.place.os.replace", fail_second
        )
        with pytest.raises(SystemExit):
            place_vs_code_payload(_payload(tmp_path / "b", skill="2"), claude)

        undo = [
            m for lv, b, m in _lines(caplog)
            if "undo" in b and lv == kamilog.CAUTION
        ]
        assert len(undo) == 1 and undo[0].startswith("restore old marketplace")
        assert (
            claude / NAME / "plugins" / "pa" / "skills" / "x" / "SKILL.md"
        ).read_text(encoding="utf-8") == "1"
