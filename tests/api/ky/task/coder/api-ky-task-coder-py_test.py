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

    # TODO

    def test0(_, opt):
        assert """### Python
Adhere to the **PEP8** style guide, ensuring clarity and consistency.""" in opt

        assert (
            """#### Docstring Style

The docstrings must be written using the **Sphinx** style and employ **reStructuredText** as the markup language. Avoid using any other styles."""
            in opt
        )

        assert (
            """#### Testing Guidelines

This section pertains specifically to Python test code. Tests should be compatible with the `pytest` module."""
            in opt
        )

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
