"""
api-ky-task-chat_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with ?role=chat
"""

import pytest


# pytest fixtures  #############################################################
@pytest.fixture
def query_string():
    return {"role": "chat"}


class TestChat:  ###############################################################

    answer_start = """# Introduction
You are **Kaye**, an AI assisting *agent* to the *user*."""

    answer_end = """# Standards
## Numerical Values with Units
- Dual Unit Systems: Present values using both the metric and US unit systems. For example:
  - Distance: `8 848m (29 029ft)`
  - Mass: `10.5kg (22 lb)`
  - Temperature: `20°C (68°F)`
- Unit Abbreviations: Always use the correct abbreviations for units to ensure clarity and precision.
- Thousands Separator: Use a space character as the thousands separator rather than a comma. For instance, express large numbers as `29 029` instead of `29,029`.

# Role"""

    # tests  ===================================================================

    def test1(self, flask_test_client, task_endpoint, query_string):
        # should be ignored
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)
        assert "# Personality" in opt

    def test_with_pls(self, flask_test_client, task_endpoint, query_string):
        # should be ignored
        query_string["programming_languages"] = "abc"

        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )
        opt = response.get_data().decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)
        assert "# Personality" in opt

    def test_no_role(self, flask_test_client, task_endpoint):
        response = flask_test_client.get(
            task_endpoint,
        )

        opt = response.get_data().decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)
        assert "# Personality" in opt

    def test_empty_role(self, flask_test_client, task_endpoint, query_string):
        query_string = {"role": ""}

        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )
        opt = response.get_data().decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)
        assert "# Personality" in opt
