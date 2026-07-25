import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def cli_command():
    return "kaye-engine "
