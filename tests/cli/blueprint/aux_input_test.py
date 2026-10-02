"""
aux_input_test.py

Unit Tests (using pytest) for:

- read_stdin_str(), detect_str_fmt(), parse_str_blueprint()
- get_name_blueprint(), get_cmd_blueprint()
"""

import io
import json

import pytest

from kaye_engine.cli.blueprint.aux_input import (
    detect_str_fmt,
    get_cmd_blueprint,
    get_name_blueprint,
    parse_str_blueprint,
    read_stdin_str,
)
from kaye_engine.prompt.blueprint import (
    Blueprint,
    blueprint_registry,
    encode_blueprint,
    register_blueprint,
)

TREE = "    ○\n[x] └── A\n"


class _FakeStdin(io.StringIO):
    def __init__(self, text, *, is_tty=False):
        super().__init__(text)
        self._is_tty = is_tty

    def isatty(self):
        return self._is_tty


@pytest.fixture
def stdin(monkeypatch):
    def _set(text, *, is_tty=False):
        monkeypatch.setattr("sys.stdin", _FakeStdin(text, is_tty=is_tty))

    return _set


@pytest.fixture
def registered():
    names = []

    def _register(name, blueprint, display_name="Display"):
        register_blueprint(
            name,
            blueprint,
            display_name=display_name,
            is_exportable=False,
        )
        names.append(name)

    yield _register

    for name in names:
        blueprint_registry.pop(name, None)


class TestReadStdin:

    def test_reads_everything(_, stdin):
        stdin("abc\ndef")

        assert read_stdin_str() == "abc\ndef"

    def test_terminal_is_an_error_not_a_hang(_, stdin):
        stdin("", is_tty=True)

        with pytest.raises(ValueError, match="terminal"):
            read_stdin_str()


class TestDetectFmt:

    @pytest.mark.parametrize(
        "text, expected",
        [
            ('{"schema": 1}', "json"),
            ('  \n\t {"schema": 1}', "json"),
            (TREE, "tree"),
            ("", "tree"),
            ("   \n", "tree"),
            ("x {", "tree"),
        ],
    )
    def test_first_non_blank_char_decides(_, text, expected):
        assert detect_str_fmt(text) == expected


class TestParseStr:

    def test_json(_):
        bp = Blueprint(nodes=frozenset({("A",)}))
        text = json.dumps(encode_blueprint(bp))

        assert parse_str_blueprint(text) == bp

    def test_tree(_):
        assert parse_str_blueprint(TREE).nodes == {("A",)}

    def test_malformed_json_raises(_):
        with pytest.raises(ValueError):
            parse_str_blueprint("{nope")


class TestGetName:

    def test_registered_name(_, registered):
        bp = Blueprint(nodes=frozenset({("A",)}))
        registered("test-aux-in-name", bp)

        assert get_name_blueprint("test-aux-in-name") == bp

    def test_unknown_name_raises(_):
        with pytest.raises(ValueError, match="unknown blueprint"):
            get_name_blueprint("no-such-blueprint")


class TestGetCmd:

    def test_name_keeps_registry_entry(_, registered):
        bp = Blueprint(nodes=frozenset({("A",)}))
        registered("test-aux-in-cmd", bp, "Cmd Display")

        out = get_cmd_blueprint("test-aux-in-cmd")

        assert out.blueprint == bp
        assert out.display_name == "Cmd Display"
        assert out.registry is blueprint_registry["test-aux-in-cmd"]

    def test_omitted_name_reads_stdin(_, stdin):
        stdin(TREE)

        out = get_cmd_blueprint(None)

        assert out.blueprint.nodes == {("A",)}
        assert out.display_name == "<stdin>"
        assert out.registry is None

    def test_omitted_name_with_terminal_raises(_, stdin):
        stdin("", is_tty=True)

        with pytest.raises(ValueError, match="terminal"):
            get_cmd_blueprint(None)

    def test_unknown_name_raises(_):
        with pytest.raises(ValueError, match="unknown blueprint"):
            get_cmd_blueprint("no-such-blueprint")
