"""
api-ky-task-coder-py.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with:

- role=coder
- PLs=py
"""

import json


import pytest

from tests.api.ky.task import *
from tests.api.ky.task.coder import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    payload = {"role": "coder", "programming_languages": "py"}

    response = flask_test_client.post(
        task_endpoint,
        data=json.dumps(payload),
        content_type="application/json",
    )

    opt = response.get_data().decode("utf-8")

    return opt


# Pytest unit tests  ###########################################################


class TestCoder:  # ============================================================

    def test_title(_, opt):
        assert "### Python" in opt

    def test_intro(_, opt):
        assert "Adhere to the **PEP8** style guide," in opt

    def test_doc0(_, opt):
        assert "##### Docstring Style" in opt

    def test_doc1(_, opt):
        assert "The docstrings must be written using the" in opt

    def test_pytest0(_, opt):
        assert "##### Testing Guidelines" in opt

    def test_pytest1(_, opt):
        assert "This section pertains specifically to Python test code" in opt

    def test_pytest2(_, opt):
        assert "*Example of tests for the `add` function:*" in opt

    # coder shared  ************************************************************

    def test_coder_title(_, opt):
        print(opt)
        assert_coder_title(opt)

    def test_coder_code_format_title(_, opt):
        print(opt)
        assert_coder_code_format_title(opt)

    def test_coder_variable_naming_title(_, opt):
        print(opt)
        assert_coder_variable_naming_title(opt)

    def test_coder_code_comment_title(_, opt):
        print(opt)
        assert_coder_code_comment_title(opt)

    def test_coder_csh_title(_, opt):
        print(opt)
        assert_coder_csh_title(opt)

    def test_style_title(_, opt):
        assert_style_title(opt)

    def test_am_title(_, opt):
        assert_am_title(opt)

    # chat blueprint  **********************************************************

    def test_intro1(_, opt):
        print(opt)
        assert_intro1(opt)

    def test_format5(_, opt):
        print(opt)
        assert_format5(opt)

    def test_personality01(_, opt):
        print(opt)
        assert_personality01(opt)

    def test_lang_title(_, opt):
        print(opt)
        assert_lang_title(opt)

    def test_element_title(_, opt):
        print(opt)
        assert_element_title(opt)

    def test_role(_, opt):
        print(opt)
        assert_role(opt)
