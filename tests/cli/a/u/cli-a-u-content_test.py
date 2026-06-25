"""
cli-a-u-content_test.py

Unit Tests (using pytest) for:

CLAUDE.md content produced by ``kaye claude user-system-prompt`` for each
flag combination (default, -r, -c, -r -c)
"""

import pytest

from tests.cli.a.u import (
    CHAT_CONTENT,
    CHAT_ABSENT,
    RAPID_CONTENT,
    RAPID_ABSENT,
    CODER_CONTENT,
    RAPID_CODER_CONTENT,
    RAPID_CODER_ABSENT,
)

# constants  ###################################################################

# BUG dont include role & abbr in these
# TODO evaluate pytest parallel

# (fixture stem, present markers, absent markers)
CASES = [
    ("chat", CHAT_CONTENT, CHAT_ABSENT),
    ("rapid", RAPID_CONTENT, RAPID_ABSENT),
    ("coder", CODER_CONTENT, []),
    ("rapid_coder", RAPID_CODER_CONTENT, RAPID_CODER_ABSENT),
]

STEMS = [stem for stem, _, _ in CASES]

PRESENT_CASES = [
    (stem, marker) for stem, present, _ in CASES for marker in present
]

ABSENT_CASES = [
    (stem, marker) for stem, _, absent in CASES for marker in absent
]


# Pytest unit tests  ###########################################################


class TestBasic:  # ============================================================

    @pytest.mark.parametrize("stem", STEMS)
    def test_existence(_, request, stem):
        assert request.getfixturevalue(stem + "_path").exists()

    @pytest.mark.parametrize("stem", STEMS)
    def test_is_file(_, request, stem):
        assert request.getfixturevalue(stem + "_path").is_file()


class TestContent:  # ==========================================================

    @pytest.mark.parametrize("stem,marker", PRESENT_CASES)
    def test_content(_, request, stem, marker):
        assert marker in request.getfixturevalue(stem + "_content")


class TestAbsent:  # ===========================================================

    @pytest.mark.parametrize("stem,marker", ABSENT_CASES)
    def test_absent(_, request, stem, marker):
        assert marker not in request.getfixturevalue(stem + "_content")
