import zipfile

import pytest

from tests.cli.a.s import prepare_root_folder

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_skills_folder(tmp_path_factory, cli_claude_command):
    command = cli_claude_command + "skill -z "
    zips_folder = prepare_root_folder(tmp_path_factory, command, "skills")
    extracted_folder = tmp_path_factory.mktemp("extracted")

    for zip_file in zips_folder.glob("*.zip"):
        with zipfile.ZipFile(zip_file) as zf:
            zf.extractall(extracted_folder)

    return extracted_folder
