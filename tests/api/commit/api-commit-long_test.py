"""
api-commit-long_test.py

Unit Tests (using pytest) for:

/kaye/dify-ap/kaye-commit-sense/per-file-long
"""

import pytest

from tests import (
    TESTEE_BRIEFNESS_CONTENT,
    TESTEE_CHAT_COMMENTARY_CASE_CONTENT,
    TESTEE_TRIAGE_TAG_BASE_CONTENT,
)
from tests.api.commit import (
    TESTEE_COMMIT_COMMON,
    TESTEE_COMMIT_PER_FILE_COMMON,
    TESTEE_COMMIT_PER_FILE_LONG,
    assert_allows_md,
    assert_no_allows_md,
)

_CONTENT = (
    TESTEE_COMMIT_COMMON
    + TESTEE_COMMIT_PER_FILE_COMMON
    + TESTEE_COMMIT_PER_FILE_LONG
    + TESTEE_BRIEFNESS_CONTENT
    + TESTEE_CHAT_COMMENTARY_CASE_CONTENT
    + TESTEE_TRIAGE_TAG_BASE_CONTENT
)


# Fixtures  ####################################################################


@pytest.fixture(scope="session")
def testee_output(flask_test_client, app_endpoint):
    response = flask_test_client.get(app_endpoint + "/per-file-long")
    return response.get_data().decode("utf-8")


@pytest.fixture(scope="session")
def endpoint(app_endpoint):
    return app_endpoint + "/per-file-long"


# Unit test classes  ###########################################################


class TestContent:  # ===========================================================

    @pytest.mark.parametrize("marker", _CONTENT)
    def test_content(_, testee_output, marker):
        assert marker in testee_output


class TestAllowsMd:  # ==========================================================

    def test_no_param(self, flask_test_client, endpoint):
        opt = flask_test_client.get(endpoint).get_data().decode("utf-8")
        assert_no_allows_md(opt)

    def test_empty_param(self, flask_test_client, endpoint):
        qs = {"allows_md": ""}
        opt = (
            flask_test_client.get(endpoint, query_string=qs)
            .get_data()
            .decode("utf-8")
        )
        assert_no_allows_md(opt)

    def test_param0(self, flask_test_client, endpoint):
        qs = {"allows_md": 0}
        opt = (
            flask_test_client.get(endpoint, query_string=qs)
            .get_data()
            .decode("utf-8")
        )
        assert_no_allows_md(opt)

    def test_param1(self, flask_test_client, endpoint):
        qs = {"allows_md": 1}
        opt = (
            flask_test_client.get(endpoint, query_string=qs)
            .get_data()
            .decode("utf-8")
        )
        assert_allows_md(opt)
