"""
api-commit-primary_test.py

Unit Tests (using pytest) for:

/kaye/dify-ap/kaye-commit-sense/primary-message
"""

import pytest


# pytest fixtures  #############################################################
@pytest.fixture
def endpoint(app_endpoint):
    return app_endpoint + "/primary-message"


# helpers  #####################################################################


class TestPrimary:  ############################################################

    # helpers  =================================================================
    def assert_common(_, opt):
        opt.startswith("""### Commentary Case
- begin 1st sentence with a lowercase letter; use standard sentence capitalization for the 2nd and subsequent sentences
- use *Title Case* for **a few important words** within a sentence
- the last sentence should not end with punctuation""")

        assert """## Briefness Style
- write in **newspaper headlinese**, prioritize brevity over grammar
- use present for current, infinitive for planned
- omit articles (a, an, the) and helper verbs, use strong nouns, verbs""" in opt
        # TODO

    def assert_allows_md(_, opt):
        assert False  # TODO

    def assert_no_md(_, opt):
        assert False  # TODO

    # no markdown  =============================================================

    def test_no_param(self, flask_test_client, endpoint):
        response = flask_test_client.get(endpoint)

        opt = response.get_data().decode("utf-8")
        print(opt)

        self.assert_common(opt)
        self.assert_no_md(opt)

    def test_empty_param(self, flask_test_client, endpoint):
        query_string = {"allows_md": ""}
        response = flask_test_client.get(endpoint, query_string=query_string)

        opt = response.get_data().decode("utf-8")
        print(opt)

        self.assert_common(opt)
        self.assert_no_md(opt)

    def test_param0(self, flask_test_client, endpoint):
        query_string = {"allows_md": 0}
        response = flask_test_client.get(endpoint, query_string=query_string)

        opt = response.get_data().decode("utf-8")
        print(opt)

        self.assert_common(opt)
        self.assert_no_md(opt)

    # w/ markdown  =============================================================

    def test_param1(self, flask_test_client, endpoint):
        query_string = {"allows_md": 1}
        response = flask_test_client.get(endpoint, query_string=query_string)

        opt = response.get_data().decode("utf-8")
        print(opt)

        self.assert_common(opt)
        self.assert_allows_md(opt)
