"""
tests/cli/github_release_parity_test.py

test: the Linux installer and ``place_vs_code_payload`` place identical
results from one payload -- ``CLAUDE.md``, the marketplace tree, and the
parsed ``settings.json`` -- fresh, over an existing install, and over
existing settings keys; the two routes are specified once in
``docs/installer-algorithm-doc.md``
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from kaye_engine.cli.claude.vs_code.place import place_vs_code_payload
from kaye_engine.cli.dry_run import disable_dry_run
from kaye_engine.cli.github_release import installer_stage
from kaye_engine.cli.github_release.installer_linux import build_linux_installer

from tests.cli.github_release_installer_windows_test import fake_payload

pytestmark = pytest.mark.skipif(
    not (shutil.which("bash") and shutil.which("python3")),
    reason="needs bash and python3",
)


# auxiliaries  #################################################################
@pytest.fixture(autouse=True)
def _fake_stage_1(monkeypatch):
    disable_dry_run()
    monkeypatch.setattr(
        installer_stage, "generate_vs_code_payload", fake_payload
    )
    yield
    disable_dry_run()


def _both_routes(tmp_path, seed=None):
    """
    run the installer under one ``HOME`` and ``place_vs_code_payload`` on
    the same payload under another, both seeded alike

    :return: the two ``.claude`` folders, installer first
    """
    payload = tmp_path / "payload"
    payload.mkdir()
    fake_payload(payload)
    run_file = tmp_path / "inst.run"
    build_linux_installer(run_file)

    homes = (tmp_path / "home-installer", tmp_path / "home-engine")
    for home in homes:
        (home / ".claude").mkdir(parents=True)
        if seed:
            seed(home / ".claude")

    subprocess.run(
        ["bash", str(run_file)],
        env=dict(os.environ, HOME=str(homes[0])),
        capture_output=True,
        check=True,
    )
    place_vs_code_payload(payload, homes[1] / ".claude")
    return homes[0] / ".claude", homes[1] / ".claude"


def _tree(claude):
    """
    every file under ``claude`` but the dated backups, as bytes, keyed by
    relative path; settings are parsed and their home path made relative
    """
    tree = {}
    for path in sorted(claude.rglob("*")):
        rel = path.relative_to(claude).as_posix()
        if not path.is_file() or rel.endswith(".bak"):
            continue
        if rel == "settings.json":
            text = path.read_text(encoding="utf-8")
            tree[rel] = json.loads(text.replace(str(claude.resolve()), "<C>"))
        else:
            tree[rel] = path.read_bytes()
    return tree


# pytest  ######################################################################
class TestParity:

    def test_fresh_claude_folder(_, tmp_path):
        installer, engine = _both_routes(tmp_path)

        assert _tree(installer) == _tree(engine)
        assert "settings.json" in _tree(installer)

    def test_existing_install_with_a_changed_prompt(_, tmp_path):
        def seed(claude):
            (claude / "CLAUDE.md").write_text("old", encoding="utf-8")

        installer, engine = _both_routes(tmp_path, seed)

        assert _tree(installer) == _tree(engine)
        for claude in (installer, engine):
            baks = list(claude.glob("CLAUDE.md.*.bak"))
            assert [b.read_text(encoding="utf-8") for b in baks] == ["old"]

    def test_existing_settings_keys(_, tmp_path):
        def seed(claude):
            (claude / "settings.json").write_text(
                json.dumps(
                    {
                        "theme": "dark",
                        "enabledPlugins": {"pa@mk": False, "x@y": True},
                    }
                ),
                encoding="utf-8",
            )

        installer, engine = _both_routes(tmp_path, seed)

        assert _tree(installer) == _tree(engine)
        settings = _tree(installer)["settings.json"]
        assert settings["enabledPlugins"] == {"pa@mk": False, "x@y": True}
        assert settings["theme"] == "dark"

    def test_stale_marketplace_file_is_dropped_by_both(_, tmp_path):
        def seed(claude):
            (claude / "mk").mkdir()
            (claude / "mk" / "stale.txt").write_text("x", encoding="utf-8")

        installer, engine = _both_routes(tmp_path, seed)

        assert _tree(installer) == _tree(engine)
        assert "mk/stale.txt" not in _tree(engine)
