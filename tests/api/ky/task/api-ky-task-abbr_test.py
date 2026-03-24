"""
api-ky-task-abbr_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with abbreviations
"""

import json

from tests.api.ky.task import _assert_rapid_blueprint_opt

# helpers  #####################################################################


def _assert_abbreviations_heading(opt):
    assert """# Abbreviations""" in opt


# pytest  ######################################################################


class TestSingle:  # ===========================================================

    def test1(self, flask_test_client, task_endpoint):
        query = "afx"
        payload = {"role": "chat", "query": query}

        response = flask_test_client.get(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")

        print(opt)

        _assert_rapid_blueprint_opt(opt)
        _assert_abbreviations_heading(opt)
        assert "- afx:affect,affected,affectedly,affectation" in opt

    # TODO more unit test


class TestMux:  # ==============================================================

    def test1(_):
        pass
