import pytest

from tests.cli.a.s import prepare_root_folder

collect_ignore = [
    "cli/a/s/cli-a-s-alts_test.py",
    "cli/c/c/cli-c-c-alts_test.py",  # hack remove/mpv CLI c c alts test
]


# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def testee_skills_folder(tmp_path_factory):
    command = "python3 -m kaye claude skill "
    return prepare_root_folder(tmp_path_factory, command, "skills")
