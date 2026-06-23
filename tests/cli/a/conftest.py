from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def cli_claude_command(cli_command):
    return cli_command + "claude "


@pytest.fixture
def mock_run():
    with patch("tests.cli.a.s.subprocess.run") as m:
        m.return_value = None
        yield m


@pytest.fixture
def mock_tmp_path():
    return Path("/tmp/kaye_mock_test")


@pytest.fixture
def mock_tmp_path_factory(mock_tmp_path):
    factory = MagicMock()
    factory.mktemp.return_value = mock_tmp_path
    return factory
