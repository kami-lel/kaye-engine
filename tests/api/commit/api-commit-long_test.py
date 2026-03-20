"""
api-commit-long_test.py

Unit Tests (using pytest) for:

/kaye/dify-ap/kaye-commit-sense/per-file-long
"""

import pytest

from tests.api.commit import (
    assert_allows_md,
    assert_no_allows_md,
    assert_per_file_common,
    assert_commit_sense_common,
)


# pytest fixtures  #############################################################
@pytest.fixture
def endpoint(app_endpoint):
    return app_endpoint + "/per-file-long"


class TestShort:  ##############################################################

    # helpers  =================================================================
    def assert_common(_, opt):
        assert """#### Long
- predominantly addition: +
- predominantly deletion: -
- mixed modification: *""" in opt

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
