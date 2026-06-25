"""
api-commit-primary_test.py

Unit Tests (using pytest) for:

/kaye/dify-ap/kaye-commit-sense/primary-message
"""

import pytest

from tests import (
    TESTEE_BRIEFNESS_CONTENT,
    TESTEE_CHAT_COMMENTARY_CASE_CONTENT,
)
from tests.api.commit import (
    TESTEE_COMMIT_COMMON,
    TESTEE_COMMIT_PRIMARY_COMMON,
    assert_allows_md,
    assert_no_allows_md,
)

_CONTENT = (
    TESTEE_COMMIT_COMMON
    + TESTEE_COMMIT_PRIMARY_COMMON
    + TESTEE_BRIEFNESS_CONTENT
    + TESTEE_CHAT_COMMENTARY_CASE_CONTENT
)


# Fixtures  ####################################################################


@pytest.fixture(scope="session")
def testee_output(flask_test_client, primary_endpoint):
    response = flask_test_client.get(primary_endpoint)
    return response.get_data().decode("utf-8")


# Unit test classes  ###########################################################


class TestContent:  # ===========================================================

    @pytest.mark.parametrize("marker", _CONTENT)
    def test_content(_, testee_output, marker):
        assert marker in testee_output


class TestAllowsMd:  # ==========================================================

    def test_no_param(self, flask_test_client, primary_endpoint):
        opt = flask_test_client.get(
            primary_endpoint
        ).get_data().decode("utf-8")
        assert_no_allows_md(opt)

    def test_empty_param(self, flask_test_client, primary_endpoint):
        qs = {"allows_md": ""}
        opt = flask_test_client.get(
            primary_endpoint, query_string=qs
        ).get_data().decode("utf-8")
        assert_no_allows_md(opt)

    def test_param0(self, flask_test_client, primary_endpoint):
        qs = {"allows_md": 0}
        opt = flask_test_client.get(
            primary_endpoint, query_string=qs
        ).get_data().decode("utf-8")
        assert_no_allows_md(opt)

    def test_param1(self, flask_test_client, primary_endpoint):
        qs = {"allows_md": 1}
        opt = flask_test_client.get(
            primary_endpoint, query_string=qs
        ).get_data().decode("utf-8")
        assert_allows_md(opt)
