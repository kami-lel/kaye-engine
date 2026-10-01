"""
export_zips_test.py

Unit Tests (using pytest) for:

export_skills_as_zips() deed logging
"""

import logging
import shutil
from unittest.mock import patch

import pytest

from kaye_engine.skill import LOGGER_SKILL_NAME
from kaye_engine.skill import export_zips
from kaye_engine.skill.export_zips import export_skills_as_zips


# auxiliaries  #################################################################
def _fake_export_folders(parent_folder, **_kwargs):
    skill_dir = parent_folder / "alpha"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("x", encoding="utf-8")


@pytest.fixture(name="_patched")
def _patched_fixture():
    with (
        patch.object(
            export_zips,
            "export_skills_as_folders",
            side_effect=_fake_export_folders,
        ),
    ):
        yield


# pytest  ######################################################################
class TestExportSkillsAsZips:

    def test_logs_create_dir_pack_and_move(_, _patched, tmp_path, caplog):
        dest = tmp_path / "out"
        with caplog.at_level(logging.INFO, logger=LOGGER_SKILL_NAME):
            export_skills_as_zips(dest, version="1")

        assert (dest / "alpha.zip").is_file()
        assert [rec.message for rec in caplog.records] == [
            "create dir {}".format(dest),
            "pack alpha -> alpha.zip",
            "move alpha.zip -> {}".format(dest / "alpha.zip"),
        ]

    def test_unwritable_destination_exits_1(_, _patched, tmp_path, caplog):
        blocker = tmp_path / "file"
        blocker.write_text("", encoding="utf-8")

        with caplog.at_level(logging.INFO, logger=LOGGER_SKILL_NAME):
            with pytest.raises(SystemExit) as info:
                export_skills_as_zips(blocker / "out", version="1")

        assert info.value.code == 1
        assert caplog.records[-1].levelno == logging.ERROR
        assert caplog.records[-1].message.startswith("fail to create dir")

    def test_archive_failure_exits_1(_, _patched, tmp_path, caplog):
        with patch.object(shutil, "make_archive", side_effect=OSError("x")):
            with caplog.at_level(logging.INFO, logger=LOGGER_SKILL_NAME):
                with pytest.raises(SystemExit) as info:
                    export_skills_as_zips(tmp_path / "out", version="1")

        assert info.value.code == 1
        assert caplog.records[-1].message.startswith("fail to pack alpha")
