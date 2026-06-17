import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def cli_claude_command(cli_command):
    return cli_command + "claude "
