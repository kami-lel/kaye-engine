"""
tests/cli/github_release_installer_windows_test.py

test: ``build_windows_installer`` -- the zip holds the payload and the two
packaged scripts byte for byte, CRLF on ``install.cmd``, no consumer name
in any template, a dry run writes nothing; with a Windows PowerShell on
the machine (WSL), ``place-payload-into-claude-folder.ps1``
runs against a sandboxed profile folder
"""

import json
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

from kaye_engine.cli.dry_run import disable_dry_run, enable_dry_run
from kaye_engine.cli.github_release import installer_stage
from kaye_engine.cli.github_release.installer_stage import (
    get_installer_template_path,
)
from kaye_engine.cli.github_release.installer_windows import (
    WINDOWS_TEMPLATE_NAMES,
    build_windows_installer,
)

_CONSUMER_NAMES = ("kaye-library", "kaye-vault", "pkg-one", "pkg-two")


# auxiliaries  #################################################################
def fake_payload(folder, *, render_profile=None):
    folder = Path(folder)
    manifest = folder / "mk" / ".claude-plugin" / "marketplace.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        json.dumps({"name": "mk", "plugins": [{"name": "pa"}]}),
        encoding="utf-8",
    )
    skill = folder / "mk" / "plugins" / "pa" / "skills" / "x" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("héllo\n", encoding="utf-8")
    (folder / "CLAUDE.md").write_text("prompt é\n", encoding="utf-8")


@pytest.fixture(autouse=True)
def _fake_stage_1(monkeypatch):
    disable_dry_run()
    monkeypatch.setattr(
        installer_stage, "generate_vs_code_payload", fake_payload
    )
    yield
    disable_dry_run()


@pytest.fixture
def built(tmp_path):
    dest = tmp_path / "inst.zip"
    build_windows_installer(dest)
    return dest


# pytest  ######################################################################
class TestWindowsInstallerZip:

    def test_zip_holds_scripts_and_payload_tree(_, built):
        with zipfile.ZipFile(built) as archive:
            assert sorted(archive.namelist()) == [
                "install.cmd",
                "payload/CLAUDE.md",
                "payload/mk/.claude-plugin/marketplace.json",
                "payload/mk/plugins/pa/skills/x/SKILL.md",
                "place-payload-into-claude-folder.ps1",
            ]

    def test_scripts_are_byte_identical_to_templates(_, built):
        with zipfile.ZipFile(built) as archive:
            for name in WINDOWS_TEMPLATE_NAMES:
                assert (
                    archive.read(name)
                    == get_installer_template_path(name).read_bytes()
                )

    def test_install_cmd_is_crlf_throughout(_):
        data = get_installer_template_path("install.cmd").read_bytes()

        assert data.count(b"\r\n") == data.count(b"\n") > 0

    def test_templates_name_no_consumer(_):
        for name in WINDOWS_TEMPLATE_NAMES:
            text = get_installer_template_path(name).read_text(
                encoding="utf-8"
            )
            for consumer in _CONSUMER_NAMES:
                assert consumer not in text

    def test_install_ps1_takes_no_parameter(_):
        text = get_installer_template_path(
            "place-payload-into-claude-folder.ps1"
        ).read_text(encoding="utf-8")

        assert "param(" not in text.lower()

    def test_dry_run_writes_nothing(_, tmp_path):
        enable_dry_run()
        dest = tmp_path / "inst.zip"

        build_windows_installer(dest)

        assert not dest.exists()


# real Windows PowerShell, when on WSL  ########################################
_POWERSHELL = shutil.which("powershell.exe")
_WSLPATH = shutil.which("wslpath")


def _win(path):
    return subprocess.run(
        [_WSLPATH, "-w", str(path)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


@pytest.mark.skipif(
    not (_POWERSHELL and _WSLPATH), reason="needs Windows PowerShell on WSL"
)
class TestInstallPs1UnderPowerShell:

    @pytest.fixture
    def sandbox(self, built, tmp_path):
        # the profile folder sits on the WSL side; PowerShell reads it
        # through its \\wsl.localhost share
        extracted = tmp_path / "extracted"
        with zipfile.ZipFile(built) as archive:
            archive.extractall(extracted)
        profile = tmp_path / "profile"
        (profile / ".claude").mkdir(parents=True)
        wrapper = tmp_path / "run.ps1"
        wrapper.write_text(
            "param($Prof, $Script)\n"
            "$env:USERPROFILE = $Prof\n"
            "& $Script\n"
            "exit $LASTEXITCODE\n",
            encoding="utf-8",
        )
        return extracted, profile, wrapper

    def _run(self, sandbox):
        extracted, profile, wrapper = sandbox
        return subprocess.run(
            [
                _POWERSHELL,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                _win(wrapper),
                "-Prof",
                _win(profile),
                "-Script",
                _win(extracted / "place-payload-into-claude-folder.ps1"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_fresh_install_then_idempotent_second_run(self, sandbox):
        _, profile, _ = sandbox
        claude = profile / ".claude"

        first = self._run(sandbox)

        assert first.returncode == 0, first.stdout + first.stderr
        assert (claude / "CLAUDE.md").read_text(
            encoding="utf-8"
        ) == "prompt é\n"
        settings = json.loads((claude / "settings.json").read_text("utf-8"))
        assert settings["enabledPlugins"] == {"pa@mk": True}
        assert "mk" in settings["extraKnownMarketplaces"]

        before = {p: p.read_bytes() for p in claude.rglob("*") if p.is_file()}
        second = self._run(sandbox)

        assert second.returncode == 0
        assert "unchanged" in second.stdout
        assert {
            p: p.read_bytes() for p in claude.rglob("*") if p.is_file()
        } == before

    def test_existing_false_and_other_keys_survive(self, sandbox):
        _, profile, _ = sandbox
        claude = profile / ".claude"
        (claude / "settings.json").write_text(
            json.dumps({"theme": "dark", "enabledPlugins": {"pa@mk": False}}),
            encoding="utf-8",
        )
        (claude / "CLAUDE.md").write_text("old", encoding="utf-8")

        result = self._run(sandbox)

        assert result.returncode == 0, result.stdout + result.stderr
        settings = json.loads((claude / "settings.json").read_text("utf-8"))
        assert settings["theme"] == "dark"
        assert settings["enabledPlugins"] == {"pa@mk": False}
        baks = list(claude.glob("CLAUDE.md.*.bak"))
        assert [b.read_text(encoding="utf-8") for b in baks] == ["old"]

    def test_invalid_settings_json_aborts_nothing_written(self, sandbox):
        _, profile, _ = sandbox
        claude = profile / ".claude"
        (claude / "settings.json").write_text("{nope", encoding="utf-8")

        result = self._run(sandbox)

        assert result.returncode != 0
        assert sorted(p.name for p in claude.iterdir()) == ["settings.json"]
