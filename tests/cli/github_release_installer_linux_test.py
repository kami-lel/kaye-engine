"""
tests/cli/github_release_installer_linux_test.py

test: ``build_linux_installer`` -- one executable file, the packaged header
byte for byte then a tar.gz of the payload; run as ``bash NAME.run`` under
a temp ``HOME``: ``CLAUDE.md``, ``.bak``, marketplace folder, settings
merge, idempotent second run, abort on invalid settings, no argument
"""

import io
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

import pytest

from kaye_engine.cli.dry_run import disable_dry_run, enable_dry_run
from kaye_engine.cli.github_release import installer_stage
from kaye_engine.cli.github_release.installer_linux import (
    LINUX_TEMPLATE_NAME,
    build_linux_installer,
)
from kaye_engine.cli.github_release.installer_stage import (
    get_installer_template_path,
)

from tests.cli.github_release_installer_windows_test import fake_payload

_MARKER = b"\n# __PAYLOAD_BELOW__\n"
_CONSUMER_NAMES = ("kaye-library", "pkg-three", "pkg-one", "pkg-two")

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


@pytest.fixture
def run_file(tmp_path):
    dest = tmp_path / "inst.run"
    build_linux_installer(dest)
    return dest


def run_installer(run_file, home, *args):
    env = dict(os.environ, HOME=str(home))
    return subprocess.run(
        ["bash", str(run_file), *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def snapshot(folder):
    return {p: p.read_bytes() for p in folder.rglob("*") if p.is_file()}


# pytest  ######################################################################
class TestLinuxInstallerFile:

    def test_header_is_the_packaged_template_byte_for_byte(_, run_file):
        header = get_installer_template_path(LINUX_TEMPLATE_NAME).read_bytes()

        assert run_file.read_bytes().startswith(header)

    def test_header_is_lf_and_ends_at_the_marker(_):
        header = get_installer_template_path(LINUX_TEMPLATE_NAME).read_bytes()

        assert b"\r" not in header
        assert header.endswith(_MARKER)

    def test_exit_precedes_the_marker(_):
        header = get_installer_template_path(LINUX_TEMPLATE_NAME).read_text(
            encoding="utf-8"
        )

        assert header.rstrip("\n").splitlines()[-2:] == [
            "exit $?",
            "# __PAYLOAD_BELOW__",
        ]

    def test_file_is_executable_mode_755(_, run_file):
        assert run_file.stat().st_mode & 0o777 == 0o755

    def test_tail_is_a_tar_gz_of_payload(_, run_file):
        header = get_installer_template_path(LINUX_TEMPLATE_NAME).read_bytes()
        archive = run_file.read_bytes()[len(header):]

        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
            names = sorted(m.name for m in tar.getmembers() if m.isfile())
            assert all(m.uid == 0 and m.gid == 0 for m in tar.getmembers())

        assert names == [
            "payload/CLAUDE.md",
            "payload/mk/.claude-plugin/marketplace.json",
            "payload/mk/plugins/pa/skills/x/SKILL.md",
        ]

    def test_template_names_no_consumer(_):
        text = get_installer_template_path(LINUX_TEMPLATE_NAME).read_text(
            encoding="utf-8"
        )

        for consumer in _CONSUMER_NAMES:
            assert consumer not in text

    def test_dry_run_writes_nothing(_, tmp_path):
        enable_dry_run()
        dest = tmp_path / "inst.run"

        build_linux_installer(dest)

        assert not dest.exists()


class TestRunUnderTempHome:

    def test_fresh_install(_, run_file, tmp_path):
        home = tmp_path / "home"
        home.mkdir()

        result = run_installer(run_file, home)

        claude = home / ".claude"
        assert result.returncode == 0, result.stdout + result.stderr
        assert (claude / "CLAUDE.md").read_text(
            encoding="utf-8"
        ) == "prompt é\n"
        skill = claude / "mk" / "plugins" / "pa" / "skills" / "x" / "SKILL.md"
        assert skill.read_text(encoding="utf-8") == "héllo\n"
        settings = json.loads((claude / "settings.json").read_text("utf-8"))
        assert settings["enabledPlugins"] == {"pa@mk": True}
        assert settings["extraKnownMarketplaces"]["mk"]["source"] == {
            "source": "directory",
            "path": os.path.realpath(claude / "mk"),
        }
        assert result.stdout.rstrip().endswith("restart VS Code")
        assert list(claude.glob("CLAUDE.md.*.bak")) == []

    def test_second_run_is_idempotent(_, run_file, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        run_installer(run_file, home)
        before = snapshot(home / ".claude")

        result = run_installer(run_file, home)

        assert result.returncode == 0
        assert "unchanged" in result.stdout
        assert snapshot(home / ".claude") == before

    def test_differing_claude_md_is_backed_up_and_kept(_, run_file, tmp_path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (home / ".claude" / "CLAUDE.md").write_text("old", encoding="utf-8")

        run_installer(run_file, home)
        run_installer(run_file, home)

        baks = list((home / ".claude").glob("CLAUDE.md.*.bak"))
        assert [b.read_text(encoding="utf-8") for b in baks] == ["old"]

    def test_existing_false_and_other_keys_survive(_, run_file, tmp_path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        settings_path = home / ".claude" / "settings.json"
        settings_path.write_text(
            json.dumps({"theme": "dark", "enabledPlugins": {"pa@mk": False}}),
            encoding="utf-8",
        )

        run_installer(run_file, home)

        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        assert settings["theme"] == "dark"
        assert settings["enabledPlugins"] == {"pa@mk": False}

    def test_invalid_settings_aborts_nothing_written(_, run_file, tmp_path):
        home = tmp_path / "home"
        (home / ".claude").mkdir(parents=True)
        (home / ".claude" / "settings.json").write_text("{nope")

        result = run_installer(run_file, home)

        assert result.returncode != 0
        assert sorted(p.name for p in (home / ".claude").iterdir()) == [
            "settings.json"
        ]

    def test_an_argument_is_rejected(_, run_file, tmp_path):
        home = tmp_path / "home"
        home.mkdir()

        result = run_installer(run_file, home, "--anything")

        assert result.returncode != 0
        assert not (home / ".claude").exists()

    def test_leaves_no_temp_folder_behind(_, run_file, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        tmpdir = tmp_path / "tmp"
        tmpdir.mkdir()
        env = dict(os.environ, HOME=str(home), TMPDIR=str(tmpdir))

        subprocess.run(
            ["bash", str(run_file)], env=env, capture_output=True, check=True
        )

        assert list(tmpdir.iterdir()) == []
