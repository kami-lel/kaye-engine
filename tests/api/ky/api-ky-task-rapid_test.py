"""
api-ky-task-rapid_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with ?role=rapid
"""

import pytest


# pytest fixtures  #############################################################
@pytest.fixture
def query_string():
    return {"role": "rapid"}


class TestRapid:  ##############################################################

    answer_start = """# Introduction
You are **Kaye**, an AI assisting *agent* to the *user*.

# Format
Please style your responses using *Github Flavored Markdown*. Avoid mentioning markdown or styling in your response.

"""

    answer_end = """For all types of **lists**, you must apply *commentary case* for **each** list item:

    <list-format-example>
    - first item
    - second item follow the Commentary Rule. And continue sentence
    </list-format-example>
"""

    # tests  ===================================================================

    def test1(self, flask_test_client, task_endpoint, query_string):
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)

    def test_with_pls(self, flask_test_client, task_endpoint, query_string):
        query_string["programming_languages"] = "abc"

        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )
        opt = response.get_data().decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)
