import subprocess

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def ce_p_command(cli_command):
    return cli_command + "continue prompt "


@pytest.fixture(scope="session")
def testee_prompts_folder(tmp_path_factory, ce_p_command):
    prompts_folder = tmp_path_factory.mktemp("prompts")

    # Execute continue export command with folder path
    cmd = ce_p_command + str(prompts_folder)
    subprocess.run(cmd, shell=True, check=True)

    return prompts_folder


@pytest.fixture(scope="session")
def header_invokable_line():
    return "invokable: true"
