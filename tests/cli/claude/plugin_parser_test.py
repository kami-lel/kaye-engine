"""
tests/cli/claude/plugin_parser_test.py

test: the ``claude plugin`` CONSUMER_PROJ positional -- parse, one-consumer
export, unknown name exits 1
"""

from argparse import ArgumentParser
from unittest.mock import patch

import pytest
from kaye_engine.cli.claude import package_meta
from kaye_engine.cli.claude.plugin.parser import register_plugin_parser
from kaye_engine.consumer import register_consumer
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, create_blueprint
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree

from tests.cli.claude.plugin_consumers_test import _FakeMetadata
from tests.consumer_helper import isolated_consumers
from tests.corpus_helper import load_corpus_from_sources


def _entry(name, consumer):
    return BlueprintRegistry(
        canonical_name=name,
        blueprint=create_blueprint(),
        consumer=consumer,
    )


@pytest.fixture(autouse=True)
def _two_consumers():
    clear_corpus_tree()
    load_corpus_from_sources(["# R\n"])
    entries = {
        "lib-skill": _entry("lib-skill", "pkg-one"),
        "app-skill": _entry("app-skill", "pkg-two"),
    }
    with isolated_consumers(), patch.dict(
        exportable_registry, entries, clear=True
    ), patch.object(package_meta, "metadata") as meta_mock:
        register_consumer("Package One", "pkg-one", "1.1.0")
        register_consumer("Package Two", "pkg-two", "2.2.0")
        meta_mock.side_effect = lambda name: _FakeMetadata(name)
        yield
    clear_corpus_tree()


def _parse(argv):
    parser = ArgumentParser()
    register_plugin_parser(parser.add_subparsers())
    return parser.parse_args(["plugin", *argv])


def _run(argv):
    args = _parse(argv)
    with patch(
        "kaye_engine.cli.claude.plugin.parser.check_setup_for_claude_cli"
    ):
        args.func(args)


class TestConsumerProjArgument:

    def test_defaults_to_none(_):
        assert _parse([]).consumer_proj is None

    def test_folder_alone_still_parses(_, tmp_path):
        args = _parse([str(tmp_path)])

        assert args.folder == tmp_path
        assert args.consumer_proj is None

    def test_second_positional_is_consumer(_, tmp_path):
        args = _parse(["-z", str(tmp_path), "pkg-two"])

        assert args.folder == tmp_path
        assert args.consumer_proj == "pkg-two"


class TestConsumerProjExport:

    def test_zip_writes_one_consumer(_, tmp_path):
        _run(["-z", str(tmp_path), "pkg-two"])

        assert [p.name for p in tmp_path.iterdir()] == ["pkg-two-claude-2.2.0.zip"]

    def test_zip_without_name_writes_every_consumer(_, tmp_path):
        _run(["-z", str(tmp_path)])

        assert len(list(tmp_path.iterdir())) == 2

    def test_folder_writes_one_consumer(_, tmp_path):
        _run([str(tmp_path), "pkg-one"])

        assert [p.name for p in tmp_path.iterdir()] == ["pkg-one"]

    def test_unknown_name_exits_1_listing_valid_names(_, tmp_path, caplog):
        with pytest.raises(SystemExit) as raised:
            _run(["-z", str(tmp_path), "pkg-nope"])

        assert raised.value.code == 1
        assert "pkg-one, pkg-two" in caplog.text
        assert list(tmp_path.iterdir()) == []
