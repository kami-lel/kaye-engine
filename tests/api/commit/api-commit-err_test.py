"""
api-commit-err_test.py

Unit Tests (using pytest) for:

errors for /kaye/dify-ap/kaye-commit-sense/*
"""

# BUG BUG update split failed this unit test


class TestParamMd:  ############################################################

    def test_bad_type(self, flask_test_client, primary_endpoint):
        query_string = {"allows_md": "abc"}
        response = flask_test_client.get(
            primary_endpoint, query_string=query_string
        )

        opt = response.get_data(as_text=True)
        print(opt)

        assert response.status_code == 422
        assert opt == "bad param: ?allows_md=abc"

    def test_bad_value(self, flask_test_client, primary_endpoint):
        query_string = {"allows_md": 150}
        response = flask_test_client.get(
            primary_endpoint, query_string=query_string
        )

        opt = response.get_data(as_text=True)
        print(opt)

        assert response.status_code == 422
        assert opt == "param ?allows_md must be 1/0: 150"
