import pytest

from tests.cli.ce.c import prepare_local_config_folder

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def ce_c_command():
    return "python3 -m kaye continue "


@pytest.fixture(scope="session")
def testee_prepared_local_config_folder(tmp_path_factory, ce_c_command):
    return prepare_local_config_folder(
        tmp_path_factory=tmp_path_factory,
        command=ce_c_command,
        folder_name="testee_local_config_folder",
    )


@pytest.fixture(scope="session")
def testee_local_config_folder(testee_prepared_local_config_folder):
    config_folder, _ = testee_prepared_local_config_folder
    return config_folder


@pytest.fixture(scope="session")
def testee_rules_folder(testee_prepared_local_config_folder):
    _, rules_folder = testee_prepared_local_config_folder
    return rules_folder
