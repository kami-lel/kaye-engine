"""
cli-a-usp-rapid_coder_test.py

Unit Tests (using pytest) for:

CLAUDE.md content produced by ``kaye claude user-system-prompt -r -c`` (rapid_coder stem)
"""

import pytest

from tests import (
    TESTEE_CODING_TERMS_ABBR,
    TESTEE_INTRODUCTION_CONTENT,
    TESTEE_MD_BASIC_FORMAT_CONTENT,
    TESTEE_MD_ADD_FORMAT_CONTENT,
    TESTEE_CODER_CONTENT,
    TESTEE_AGENT_BEHAVIOR_CONTENT,
    TESTEE_TRIAGE_TAG_CONTENT,
)
from tests.cli.a import TESTEE_CLAUDE_BEHAVIOR_CONTENT

# Fixtures  ####################################################################


@pytest.fixture(scope="session")
def content(rapid_coder_content):
    return rapid_coder_content


# Unit test classes  ###########################################################


class TestBasic:  # ============================================================

    def test_existence(self, rapid_coder_path):
        assert rapid_coder_path.exists()

    def test_is_file(self, rapid_coder_path):
        assert rapid_coder_path.is_file()


class TestContent:  # ===========================================================

    @pytest.mark.parametrize("marker", TESTEE_INTRODUCTION_CONTENT)
    def test_introduction(self, content, marker):
        assert marker in content

    @pytest.mark.parametrize("marker", TESTEE_MD_BASIC_FORMAT_CONTENT)
    def test_md_basic_format(self, content, marker):
        assert marker in content

    @pytest.mark.parametrize("marker", TESTEE_MD_ADD_FORMAT_CONTENT)
    def test_md_add_format(self, content, marker):
        assert marker in content

    @pytest.mark.parametrize("marker", TESTEE_CODER_CONTENT)
    def test_coder(self, content, marker):
        assert marker in content

    @pytest.mark.parametrize("marker", TESTEE_TRIAGE_TAG_CONTENT)
    def test_triage_tags(self, content, marker):
        assert marker in content

    @pytest.mark.parametrize("marker", TESTEE_CODING_TERMS_ABBR)
    def test_coding_terms(self, content, marker):
        assert marker in content

    @pytest.mark.parametrize("marker", TESTEE_AGENT_BEHAVIOR_CONTENT)
    def test_agent_behavior(self, content, marker):
        assert marker in content

    @pytest.mark.parametrize("marker", TESTEE_CLAUDE_BEHAVIOR_CONTENT)
    def test_claude_behavior(self, content, marker):
        assert marker in content
