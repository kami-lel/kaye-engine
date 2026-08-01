"""
package_version_test.py

Unit Tests (using pytest) for:

resolve_package_version
"""

from importlib.metadata import PackageNotFoundError
from unittest.mock import patch

import pytest

from kaye_engine.cli.claude.package_version import resolve_package_version


# pytest  ######################################################################
class TestResolvePackageVersion:

    def test_returns_installed_version(_):
        with patch(
            "kaye_engine.cli.claude.package_version.version",
            return_value="1.2.3",
        ):
            assert resolve_package_version() == "1.2.3"

    def test_raises_system_exit_when_not_installed(_):
        with patch(
            "kaye_engine.cli.claude.package_version.version",
            side_effect=PackageNotFoundError,
        ):
            with pytest.raises(SystemExit):
                resolve_package_version()
