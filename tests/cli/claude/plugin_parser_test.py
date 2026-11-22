"""
tests/cli/claude/plugin_parser_test.py

test: the ``claude plugin`` --consumer, --all options -- parse, one-consumer
export, absent means the default consumer, unknown name exits 1
"""

from argparse import ArgumentParser
from unittest.mock import patch

import pytest
from kaye_engine.cli.plugin_platform import package_meta
from kaye_engine.cli.claude.plugin.parser import register_plugin_parser
from kaye_engine.consumer import register_consumer, set_default_consumer
from kaye_engine.repo import set_repo_name, set_repo_version
from kaye_engine.exportable import exportable_registry
from kaye_engine.prompt.blueprint import BlueprintRegistry, create_blueprint
from kaye_engine.prompt.prompt_corpus_loader import clear_corpus_tree

from tests.cli.claude.plugin_consumers_test import _FakeMetadata
from tests.consumer_helper import isolated_consumers, isolated_repo
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
    with isolated_consumers(), isolated_repo(), patch.dict(
        exportable_registry, entries, clear=True
    ), patch.object(package_meta, "metadata") as meta_mock:
        register_consumer("Package One", "pkg-one", "1.1.0")
        register_consumer("Package Two", "pkg-two", "2.2.0")
        set_default_consumer("pkg-one")
        set_repo_name("pkg-one")
        set_repo_version("1.1.0")
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


class TestConsumerArgument:

    def test_defaults_to_none_and_not_all(_):
        args = _parse([])

        assert args.consumer is None
        assert args.all_consumers is False

    def test_folder_alone_still_parses(_, tmp_path):
        args = _parse([str(tmp_path)])

        assert args.folder == tmp_path
        assert args.consumer is None

    def test_consumer_option_takes_several_names(_, tmp_path):
        args = _parse(
            ["-z", str(tmp_path), "--consumer", "pkg-two", "pkg-one"]
        )

        assert args.folder == tmp_path
        assert args.consumer == ["pkg-two", "pkg-one"]

    def test_all_flag_long_and_short(_):
        assert _parse(["--all"]).all_consumers is True
        assert _parse(["-a"]).all_consumers is True

    def test_old_second_positional_is_rejected(_, tmp_path):
        with pytest.raises(SystemExit):
            _parse(["-z", str(tmp_path), "pkg-two"])

    def test_consumer_with_all_is_rejected(_):
        with pytest.raises(SystemExit):
            _parse(["--consumer", "pkg-two", "--all"])


class TestConsumerExport:

    def test_zip_writes_one_consumer(_, tmp_path):
        _run(["-z", str(tmp_path), "--consumer", "pkg-two"])

        assert [p.name for p in tmp_path.iterdir()] == [
            "pkg-one-1.1.0-claude-desktop-plugin-pkg-two.zip"
        ]

    def test_zip_writes_several_consumers(_, tmp_path):
        _run(["-z", str(tmp_path), "--consumer", "pkg-two", "pkg-one"])

        assert sorted(p.name for p in tmp_path.iterdir()) == sorted(
            [
                "pkg-one-1.1.0-claude-desktop-plugin.zip",
                "pkg-one-1.1.0-claude-desktop-plugin-pkg-two.zip",
            ]
        )

    def test_all_writes_every_plugin_consumer(_, tmp_path):
        _run(["-z", str(tmp_path), "-a"])

        assert len(list(tmp_path.iterdir())) == 2

    def test_all_writes_every_folder(_, tmp_path):
        _run([str(tmp_path), "--all"])

        assert sorted(p.name for p in tmp_path.iterdir()) == [
            "pkg-one",
            "pkg-two",
        ]

    def test_zip_without_name_writes_the_default_consumer(_, tmp_path):
        _run(["-z", str(tmp_path)])

        assert [p.name for p in tmp_path.iterdir()] == [
            "pkg-one-1.1.0-claude-desktop-plugin.zip"
        ]

    def test_folder_without_name_writes_the_default_consumer(_, tmp_path):
        _run([str(tmp_path)])

        assert [p.name for p in tmp_path.iterdir()] == ["pkg-one"]

    def test_absent_name_with_no_default_consumer_exits_1(_, tmp_path):
        # pylint: disable=import-outside-toplevel
        from kaye_engine import consumer

        consumer._default_canonical_name = None

        with pytest.raises(SystemExit) as raised:
            _run(["-z", str(tmp_path)])

        assert raised.value.code == 1
        assert list(tmp_path.iterdir()) == []

    def test_folder_writes_one_consumer(_, tmp_path):
        _run([str(tmp_path), "--consumer", "pkg-one"])

        assert [p.name for p in tmp_path.iterdir()] == ["pkg-one"]

    def test_unknown_name_exits_1_listing_valid_names(_, tmp_path, caplog):
        with pytest.raises(SystemExit) as raised:
            _run(["-z", str(tmp_path), "--consumer", "pkg-nope"])

        assert raised.value.code == 1
        assert "pkg-one, pkg-two" in caplog.text
        assert list(tmp_path.iterdir()) == []
