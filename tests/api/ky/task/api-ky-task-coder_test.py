"""
api-ky-task-coder_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=coder
"""

import json


from tests.api.ky.task import _assert_chat_blueprint_opt
from tests.api import assert_briefness_style, assert_annotation_markers

# helper  ######################################################################


def _assert_coder_basic_blueprint_opt(opt):
    _assert_chat_blueprint_opt(opt)
    assert_briefness_style(opt)
    assert_annotation_markers(opt)

    assert (
        """# Style
## Capitalization
### Title Case
Use *Chicago Manual of Style* headline case:

- **capitalize major words**: nouns, pronouns, verbs, adjectives, adverbs, numerals"""
        in opt
    )

    assert (
        """## Kaye Peer Coder
Duties are as follows:

- provide code **expansion** per user instructions while maintaining formatting and naming consistency with provided examples and excluding those examples from your response"""
        in opt
    )

    assert "#### variable naming" in opt

    assert "#### code comment" in opt

    assert "#### comment section headings" in opt

    assert "# parser.py" in opt


def _assert_c_opt(opt):
    assert """### C
Use **C99** standard""" in opt


def _assert_cpp_opt(opt):
    assert """### C++
use **C++17** standard""" in opt


def _assert_u3d_opt(opt):
    assert "### Unity Engine" in opt
    assert "Unity **6**" in opt
    assert "#### MonoBehaviour" in opt
    assert "never mixed into *Private Methods*" in opt


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


def assert_bash(opt):
    """### Bash

You write command lines for Debian GNU/Linux only.""" in opt


class TestBase:  ###############################################################

    # tests  ===================================================================

    def test_no_plc(_, flask_test_client, task_endpoint):
        payload = {"role": "coder"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)

    def test_empty_plc1(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": ""}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)

    def test_empty_plc2(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": ","}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)


class TestIndv:  ###############################################################

    def test_c(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "c"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_c_opt(opt)

    def test_cpp(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "cpp"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_c_opt(opt)
        _assert_cpp_opt(opt)

    def test_ue(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "ue"}
        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_c_opt(opt)
        _assert_cpp_opt(opt)
        _assert_ue_opt(opt)

    def test_cs(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "csharp"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_cs_opt(opt)

    def test_u3d(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "u3d"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_cs_opt(opt)
        _assert_u3d_opt(opt)

    def test_gd(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "gdscript"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_gd_opt(opt)

    def test_html(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "html"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_html_opt(opt)

    def test_js(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "js"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_js_ts_opt(opt)

    def test_ts(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "ts"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_js_ts_opt(opt)

    def test_qt(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "qt"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_qt_opt

    def test_qml(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "qml"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_qt_opt
        _assert_qml_opt

    def test_py(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "py"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_py_opt(opt)

    def test_bash(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "bash"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        assert_bash(opt)


class TestMux:  ################################################################

    def test1(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "c,cpp,ue"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_c_opt(opt)
        _assert_cpp_opt(opt)
        _assert_ue_opt(opt)

    def test2(_, flask_test_client, task_endpoint):
        payload = {
            "role": "coder",
            "programming_languages": "gdscript,html,js,qt",
        }

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_gd_opt(opt)
        _assert_html_opt(opt)
        _assert_js_ts_opt(opt)
        _assert_qt_opt(opt)

    def test3(_, flask_test_client, task_endpoint):
        payload = {"role": "coder", "programming_languages": "py,qt,u3d"}

        response = flask_test_client.post(
            task_endpoint,
            data=json.dumps(payload),
            content_type="application/json",
        )

        opt = response.get_data().decode("utf-8")
        print(opt)

        _assert_chat_blueprint_opt(opt)
        _assert_coder_basic_blueprint_opt(opt)
        _assert_py_opt(opt)
        _assert_qt_opt(opt)
        _assert_cs_opt(opt)
        _assert_u3d_opt(opt)
