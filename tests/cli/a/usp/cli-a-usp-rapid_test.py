"""
cli-a-usp-rapid_test.py

Unit Tests (using pytest) for:

CLAUDE.md content produced by ``kaye claude user-system-prompt -r`` (rapid stem)
"""

import pytest

from tests import (
    TESTEE_MD_BASIC_FORMAT_CONTENT,
    TESTEE_MD_ADD_FORMAT_CONTENT,
    TESTEE_AGENT_BEHAVIOR_CONTENT,
)
from tests.cli.a import TESTEE_CLAUDE_BEHAVIOR_CONTENT


# Fixtures  ####################################################################


@pytest.fixture(scope="session")
def content(rapid_content):
    return rapid_content


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_existence(self, rapid_path):
        assert rapid_path.exists()

    def test_is_file(self, rapid_path):
        assert rapid_path.is_file()


class TestContent:  # ===========================================================

    @pytest.mark.parametrize("marker", TESTEE_MD_BASIC_FORMAT_CONTENT)
    def test_md_basic_format(self, content, marker):
        assert marker in content

    @pytest.mark.parametrize("marker", TESTEE_MD_ADD_FORMAT_CONTENT)
    def test_md_add_format(self, content, marker):
        assert marker in content

    @pytest.mark.parametrize("marker", TESTEE_AGENT_BEHAVIOR_CONTENT)
    def test_agent_behavior(self, content, marker):
        assert marker in content

    @pytest.mark.parametrize("marker", TESTEE_CLAUDE_BEHAVIOR_CONTENT)
    def test_claude_behavior(self, content, marker):
        assert marker in content
