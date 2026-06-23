"""
cli-a-sz-alts-a-s_test.py

Unit Tests (using pytest) for:

CLI alias: ``python -m kaye a s -z`` (both claude and skill aliases, create .zip packages)
Verifies all skill .zip files are exported.
"""

import pytest

from tests.cli.a import ALL_CLAUDE_SKILL_NAMES
from tests.cli.a.s import prepare_root_folder


# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_zips_folder(tmp_path_factory, cli_command):
    command = cli_command + "a s -z "
    return prepare_root_folder(
        tmp_path_factory=tmp_path_factory,
        command=command,
        folder_name="zips_a_s",
    )


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_zips_folder_exists(self, testee_zips_folder):
        assert testee_zips_folder.exists()

    def test_zips_folder_is_dir(self, testee_zips_folder):
        assert testee_zips_folder.is_dir()


class TestZipFiles:  # =========================================================

    @pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)
    def test_zip_file_exists(self, testee_zips_folder, skill_name):
        zip_file = testee_zips_folder / f"{skill_name}.zip"
        assert zip_file.exists(), f"Missing {skill_name}.zip"

    @pytest.mark.parametrize("skill_name", ALL_CLAUDE_SKILL_NAMES)
    def test_zip_file_is_file(self, testee_zips_folder, skill_name):
        zip_file = testee_zips_folder / f"{skill_name}.zip"
        assert zip_file.is_file(), f"{skill_name}.zip is not a file"
