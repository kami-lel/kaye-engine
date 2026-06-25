"""
api-commit-short_test.py

Unit Tests (using pytest) for:

/kaye/dify-ap/kaye-commit-sense/per-file-short
"""

import pytest

from tests.api.commit import (
    assert_allows_md,
    assert_no_allows_md,
    assert_per_file_common,
    assert_commit_sense_common,
)

# TODO better improved


# pytest fixtures  #############################################################
@pytest.fixture
def endpoint(app_endpoint):
    return app_endpoint + "/per-file-short"


@pytest.fixture(scope="session")
def testee_output(flask_test_client, app_endpoint):
    endpoint = app_endpoint + "/per-file-short"
    response = flask_test_client.get(endpoint)
    return response.get_data().decode("utf-8")


# TT (Triage Tags)  #############################################################

_TT_CONTENT = [
    (
        "## Triage Tags\n\nLabels for defects and related notes across code and"
        " docs; refer to them as *triage tags* or *TT*."
    ),
    "- `BUG` — discovered defects that cause errors or unexpected behavior",
]


class TestTriageTags:  # ========================================================

    @pytest.mark.parametrize("i", range(len(_TT_CONTENT)))
    def test_tt_content(_, testee_output, i):
        assert _TT_CONTENT[i] in testee_output


class TestShort:  ##############################################################

    # helpers  =================================================================
    def assert_common(_, opt):
        assert """#### Short
- predominantly addition: /""" in opt

    # no markdown  =============================================================

    def test_no_param(self, flask_test_client, endpoint):
        response = flask_test_client.get(endpoint)

        opt = response.get_data().decode("utf-8")
        print(opt)

        assert_commit_sense_common(opt)
        assert_per_file_common(opt)
        self.assert_common(opt)
        assert_no_allows_md(opt)

    def test_empty_param(self, flask_test_client, endpoint):
        query_string = {"allows_md": ""}
        response = flask_test_client.get(endpoint, query_string=query_string)

        opt = response.get_data().decode("utf-8")
        print(opt)

        assert_commit_sense_common(opt)
        assert_per_file_common(opt)
        self.assert_common(opt)
        assert_no_allows_md(opt)

    def test_param0(self, flask_test_client, endpoint):
        query_string = {"allows_md": 0}
        response = flask_test_client.get(endpoint, query_string=query_string)

        opt = response.get_data().decode("utf-8")
        print(opt)

        assert_commit_sense_common(opt)
        assert_per_file_common(opt)
        self.assert_common(opt)
        assert_no_allows_md(opt)

    # w/ markdown  =============================================================

    def test_param1(self, flask_test_client, endpoint):
        query_string = {"allows_md": 1}
        response = flask_test_client.get(endpoint, query_string=query_string)

        opt = response.get_data().decode("utf-8")
        print(opt)

        assert_commit_sense_common(opt)
        assert_per_file_common(opt)
        self.assert_common(opt)
        assert_allows_md(opt)
