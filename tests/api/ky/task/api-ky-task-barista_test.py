"""
api-ky-task-barista_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with ?role=barista
"""

import pytest

from tests.api.ky.task import _assert_rapid_blueprint_opt


# pytest fixtures  #############################################################
@pytest.fixture
def query_string():
    return {"role": "barista"}


# pytest  ######################################################################
class TestBarista:

    def test1(_, flask_test_client, task_endpoint, query_string):
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")

        print(opt)

        _assert_rapid_blueprint_opt(opt)

        assert (
            """## Date & Time Format
- Full Date Example: For dates with a specific year, format them as: `Mon 02015-01-15` (Day of the week 0Year-Month-Day)."""
            in opt
        )

        assert (
            """## Assistant Barista
Maintain a coffee brewing note document for a coffee product, its batch/bag, and brew sessions, including user experience.

Transform any user-provided input into the required document format using only provided information."""
            in opt
        )

        assert """### document structure
#### Level 1: Document Title
Include only heading, must be exactly: `# Coffee Brewing Note`""" in opt
