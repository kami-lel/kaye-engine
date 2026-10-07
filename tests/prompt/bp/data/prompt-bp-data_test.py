"""
prompt-bp-data_test.py

Unit Tests (using pytest) for:

Blueprint, BlueprintMeta, create_blueprint, encode_blueprint,
decode_blueprint, load_blueprint, save_blueprint
"""

import dataclasses
import json
import pickle
import subprocess
import sys

import pytest

from kaye_engine.prompt.blueprint.data import (
    Blueprint,
    BlueprintMeta,
    create_blueprint,
    decode_blueprint,
    dump_blueprint,
    encode_blueprint,
    load_blueprint,
    parse_blueprint_json,
    save_blueprint,
)


# pytest fixtures  #############################################################
@pytest.fixture
def blueprint():
    return Blueprint(
        meta=BlueprintMeta(
            display_name="Thing Doer",
            description="Does things",
            globs_node=("Style", "{globs}"),
        ),
        nodes=frozenset({("A", "B"), ("C",)}),
        subtrees=frozenset({("Amanuensis", "Redactor")}),
        dependencies=(
            "coder",
            Blueprint(nodes=frozenset({("X",)}), dependencies=("deep",)),
        ),
    )


# pytest  ######################################################################
class TestValue:

    def test_defaults_are_empty(_):
        bp = Blueprint()

        assert bp.nodes == frozenset()
        assert bp.subtrees == frozenset()
        assert bp.dependencies == ()
        assert bp.meta == BlueprintMeta()

    def test_frozen(_):
        with pytest.raises(dataclasses.FrozenInstanceError):
            Blueprint().nodes = frozenset()

    def test_equal_hash_equal(_, blueprint):
        twin = dataclasses.replace(blueprint)

        assert twin == blueprint
        assert hash(twin) == hash(blueprint)
        assert len({twin, blueprint}) == 1

    def test_unequal(_, blueprint):
        assert dataclasses.replace(blueprint, nodes=frozenset()) != blueprint


class TestCreate:

    def test_empty(_):
        assert create_blueprint() == Blueprint()

    def test_full_is_one_root_subtree(_):
        assert create_blueprint(is_full=True).subtrees == frozenset({()})

    def test_dependencies_become_tuple(_):
        assert create_blueprint(dependencies=["a", "b"]).dependencies == (
            "a",
            "b",
        )


class TestJson:

    def test_round_trip(_, blueprint):
        assert decode_blueprint(encode_blueprint(blueprint)) == blueprint

    def test_round_trip_through_text(_, blueprint):
        text = json.dumps(encode_blueprint(blueprint))

        assert parse_blueprint_json(text) == blueprint

    def test_envelope_carries_schema(_, blueprint):
        assert encode_blueprint(blueprint)["schema"] == 1

    def test_encoding_is_deterministic(_, blueprint):
        shuffled = dataclasses.replace(
            blueprint, nodes=frozenset(reversed(sorted(blueprint.nodes)))
        )

        assert encode_blueprint(shuffled) == encode_blueprint(blueprint)

    def test_hand_written(_):
        bp = decode_blueprint(
            {
                "schema": 1,
                "meta": {"description": "x"},
                "nodes": [["Style Guide", "Markdown"]],
                "subtrees": [["Amanuensis", "Redactor"]],
                "dependencies": ["coder"],
            }
        )

        assert bp.meta.description == "x"
        assert bp.nodes == frozenset({("Style Guide", "Markdown")})
        assert bp.subtrees == frozenset({("Amanuensis", "Redactor")})
        assert bp.dependencies == ("coder",)

    def test_minimal_hand_written(_):
        assert decode_blueprint({"schema": 1}) == Blueprint()

    def test_display_name_round_trips(_, blueprint):
        encoded = encode_blueprint(blueprint)

        assert encoded["meta"]["display_name"] == "Thing Doer"
        assert decode_blueprint(encoded).meta.display_name == "Thing Doer"

    def test_absent_display_name_decodes_empty(_):
        bp = decode_blueprint({"schema": 1, "meta": {"description": "x"}})

        assert bp.meta.display_name == ""

    def test_empty_display_name_not_encoded(_):
        assert "display_name" not in encode_blueprint(Blueprint())["meta"]

    @pytest.mark.parametrize(
        "data",
        [
            {},
            {"schema": 2},
            {"schema": 1, "nodes": [["ok", 3]]},
            {"schema": 1, "nodes": ["flat"]},
            {"schema": 1, "meta": {"description": 4}},
            {"schema": 1, "meta": {"display_name": 4}},
            [],
            "not json",
            '{"schema": 1}',
        ],
    )
    def test_malformed_raises(_, data):
        with pytest.raises(ValueError):
            decode_blueprint(data)

    def test_file_round_trip(_, blueprint, tmp_path):
        path = tmp_path / "bp.json"

        save_blueprint(blueprint, path)

        assert load_blueprint(path) == blueprint

    def test_decode_needs_no_corpus(_):
        # no corpus is loaded by this suite: decoding must still work
        assert decode_blueprint({"schema": 1, "nodes": [["A"]]}).nodes


class TestDump:

    def test_round_trip(_, blueprint):
        assert parse_blueprint_json(dump_blueprint(blueprint)) == blueprint

    def test_ends_with_newline(_, blueprint):
        assert dump_blueprint(blueprint).endswith("}\n")

    def test_indent_applies(_):
        assert '\n    "schema"' in dump_blueprint(Blueprint(), indent=4)

    def test_save_writes_dump(_, blueprint, tmp_path):
        path = tmp_path / "bp.json"
        save_blueprint(blueprint, path)

        assert path.read_text(encoding="utf-8") == dump_blueprint(blueprint)


class TestParseJson:

    def test_parses_dumped_text(_):
        blueprint = Blueprint(nodes=frozenset({("A",)}))
        text = json.dumps(encode_blueprint(blueprint))

        assert parse_blueprint_json(text) == blueprint

    def test_malformed_json_raises(_):
        with pytest.raises(ValueError, match="not valid JSON"):
            parse_blueprint_json("{nope")

    def test_unknown_schema_raises(_):
        with pytest.raises(ValueError, match="schema"):
            parse_blueprint_json('{"schema": 99}')


class TestPickle:

    def test_round_trip(_, blueprint):
        assert pickle.loads(pickle.dumps(blueprint)) == blueprint

    @pytest.mark.parametrize("seed", ["0", "1", "12345"])
    def test_fresh_process_and_hash_seed(_, blueprint, seed):
        script = (
            "import pickle,sys,json;"
            "from kaye_engine.prompt.blueprint.data import *;"
            "bp=pickle.loads(sys.stdin.buffer.read());"
            "print(json.dumps(encode_blueprint(bp),sort_keys=True))"
        )
        done = subprocess.run(
            [sys.executable, "-c", script],
            input=pickle.dumps(blueprint),
            capture_output=True,
            env={"PYTHONHASHSEED": seed, "PATH": ""},
            check=True,
        )

        assert json.loads(done.stdout) == json.loads(
            json.dumps(encode_blueprint(blueprint), sort_keys=True)
        )


