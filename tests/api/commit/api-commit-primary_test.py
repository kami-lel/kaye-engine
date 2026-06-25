"""
api-commit-primary_test.py

Unit Tests (using pytest) for:

/kaye/dify-ap/kaye-commit-sense/primary-message
"""

from tests.api.commit import (
    assert_allows_md,
    assert_no_allows_md,
    assert_commit_sense_common,
)


class TestPrimary:  ############################################################

    # helpers  =================================================================
    def assert_common(_, opt):
        assert """## Primary Message Task
Produce a concise summary of changes across **multiple** files.""" in opt

    # no markdown  =============================================================

    def test_no_param(self, flask_test_client, primary_endpoint):
        response = flask_test_client.get(primary_endpoint)

        opt = response.get_data().decode("utf-8")

        assert_commit_sense_common(opt)
        self.assert_common(opt)
        assert_no_allows_md(opt)

    def test_empty_param(self, flask_test_client, primary_endpoint):
        query_string = {"allows_md": ""}
        response = flask_test_client.get(
            primary_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")

        assert_commit_sense_common(opt)
        self.assert_common(opt)
        assert_no_allows_md(opt)

    def test_param0(self, flask_test_client, primary_endpoint):
        query_string = {"allows_md": 0}
        response = flask_test_client.get(
            primary_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")

        assert_commit_sense_common(opt)
        self.assert_common(opt)
        assert_no_allows_md(opt)

    # w/ markdown  =============================================================

    def test_param1(self, flask_test_client, primary_endpoint):
        query_string = {"allows_md": 1}
        response = flask_test_client.get(
            primary_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")

        assert_commit_sense_common(opt)
        self.assert_common(opt)
        assert_allows_md(opt)
