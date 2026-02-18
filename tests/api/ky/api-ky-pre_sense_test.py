"""
api-dify-ky-pre_sense_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/pre-sense
"""

import pytest


# pytest fixtures  #############################################################
@pytest.fixture
def local_endpoint(app_endpoint):
    return app_endpoint + "/pre-sense"


class TestNoRole:

    def test1(_, flask_test_client, local_endpoint):
        # BUG

        response = flask_test_client.get(local_endpoint)
        opt = response.data.decode("utf-8")

        print(opt)
        assert opt.startswith("AAA")
        assert opt.endswith("ZZZ")


class TestCoder:  ##############################################################

    def test1(_, flask_test_client, local_endpoint):
        # BUG

        response = flask_test_client.get(
            local_endpoint, query_string={"role": "peer_coder"}
        )
        opt = response.data.decode("utf-8")

        print(opt)
        assert opt.startswith("AAA")
        assert opt.endswith("ZZZ")
