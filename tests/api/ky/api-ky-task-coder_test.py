"""
api-ky-task-coder_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with ?role=coder
"""

import pytest

from tests.api.ky import _assert_chat_blueprint_opt

# BUG, use blueprint


# pytest fixtures  #############################################################
@pytest.fixture
def query_string():
    return {"role": "coder"}


# helper  ######################################################################


def _assert_coder_basic_blueprint_opt(opt):
    _assert_chat_blueprint_opt(opt)

    assert (
        """## Kaye Peer Coder
Duties are as follows:

- provide code **expansion** per user instructions while maintaining formatting and naming consistency with provided examples and excluding those examples from your response"""
        in opt
    )

    assert (
        """#### Variable naming

- use i, j, k for loop counters, for example `for (int i = 1; i <= 5; i++)`"""
        in opt
    )

    assert (
        """#### Code comment

- format inline comments as: actual code + two spaces + `#` or `//` + single space + comment content, for example `int a = 1;  // comment on number`"""
        in opt
    )

    assert (
        """Use **comment section headings** *only inside code comments* to show structure (file info, modules, sections, functions) **when they materially improve readability**."""
        in opt
    )


def _assert_c_opt(opt):
    assert """### C
Use **C99** standard""" in opt


def _assert_cpp_opt(opt):
    assert """### C++
use **C++17** standard""" in opt


def _assert_u3d_opt(opt):
    assert """### Unity Engine
- Version: `6000.0.34f1`
- Documentation: Employ XML documentation comments""" in opt


def _assert_ue_opt(opt):
    assert """### Unreal Engine
- Version: Unreal Engine `5.6.0`""" in opt


def _assert_cs_opt(opt):
    assert (
        """### C Sharp
- Documentation: Use XML comments (`/// <summary>...</summary>`) to document functionality and provide examples wherever helpful."""
        in opt
    )


def _assert_gd_opt(opt):
    assert """### GDScript
- Version: Godot 4""" in opt


def _assert_html_opt(opt):
    assert """### HTML
- Version: **HTML5** standard""" in opt


def _assert_qt_opt(opt):
    assert """### Qt
This section is solely for Qt framework.
""" in opt


def _assert_js_ts_opt(opt):
    assert (
        """### JavaScript & TypeScript
These standards are applicable exclusively to JavaScript and TypeScript code, adhering to the **ES11** standard."""
        in opt
    )


def _assert_qml_opt(opt):
    assert """#### QML
Declarations of items must follow this order:

1. id""" in opt


def _assert_py_opt(opt):
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


class TestBase:  ###############################################################

    # tests  ===================================================================

    def test_no_plc(_, flask_test_client, task_endpoint, query_string):
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)

    def test_empty_plc1(_, flask_test_client, task_endpoint, query_string):
        query_string["programming_languages"] = ""
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)

    def test_empty_plc2(_, flask_test_client, task_endpoint, query_string):
        query_string["programming_languages"] = ","
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)


class TestIndv:  ###############################################################

    def test_c(_, flask_test_client, task_endpoint, query_string):
        pls = "c"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_c_opt(opt)

    def test_cpp(_, flask_test_client, task_endpoint, query_string):
        pls = "cpp"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_c_opt(opt)
        _assert_cpp_opt(opt)

    def test_ue(_, flask_test_client, task_endpoint, query_string):
        pls = "ue"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_c_opt(opt)
        _assert_cpp_opt(opt)
        _assert_ue_opt(opt)

    def test_cs(_, flask_test_client, task_endpoint, query_string):
        pls = "csharp"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_cs_opt(opt)

    def test_u3d(_, flask_test_client, task_endpoint, query_string):
        pls = "u3d"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_cs_opt(opt)
        _assert_u3d_opt(opt)

    def test_gd(_, flask_test_client, task_endpoint, query_string):
        pls = "gdscript"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_gd_opt(opt)

    def test_html(_, flask_test_client, task_endpoint, query_string):
        pls = "html"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_html_opt(opt)

    def test_js(_, flask_test_client, task_endpoint, query_string):
        pls = "js"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_js_ts_opt(opt)

    def test_ts(_, flask_test_client, task_endpoint, query_string):
        pls = "ts"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_js_ts_opt(opt)

    def test_qt(_, flask_test_client, task_endpoint, query_string):
        pls = "qt"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_qt_opt

    def test_qml(_, flask_test_client, task_endpoint, query_string):
        pls = "qml"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_qt_opt
        _assert_qml_opt

    def test_py(_, flask_test_client, task_endpoint, query_string):
        pls = "py"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_py_opt(opt)

    def test_console(_, flask_test_client, task_endpoint, query_string):
        pls = "console"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        assert """### Message Level
These keywords indicate the severity of a message:""" in opt


class TestMux:  ################################################################

    def test1(_, flask_test_client, task_endpoint, query_string):
        pls = "c,cpp,ue"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_c_opt(opt)
        _assert_cpp_opt(opt)
        _assert_ue_opt(opt)

    def test2(_, flask_test_client, task_endpoint, query_string):
        pls = "gdscript,html,js,qt"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_gd_opt(opt)
        _assert_html_opt(opt)
        _assert_js_ts_opt(opt)
        _assert_qt_opt(opt)

    def test3(_, flask_test_client, task_endpoint, query_string):
        pls = "py,qt,u3d"

        query_string["programming_languages"] = pls
        response = flask_test_client.get(
            task_endpoint, query_string=query_string
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_py_opt(opt)
        _assert_qt_opt(opt)
        _assert_cs_opt(opt)
        _assert_u3d_opt(opt)
