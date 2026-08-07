"""
tests/cli/dynamic_node/parser_test.py

Unit Tests (using pytest) for:

_dynamic_node_main, register_dynamic_node_parser
"""

from argparse import ArgumentParser

import pytest

from kaye_engine.cli.dynamic_node import parser as dynamic_node_parser
from kaye_engine.prompt.dynamic_nodes import AbbrGroupNode
from kaye_engine.prompt.prompt_corpus_node import PromptCorpusNode


# auxiliaries  ##################################################################
def _build_dn_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    dynamic_node_parser.register_dynamic_node_parser(subparser)
    return root_parser


@pytest.fixture(autouse=True)
def _no_stdin_query(monkeypatch):
    # NODE handlers probe ``sys.stdin.isatty()`` to optionally read a
    # query from stdin; pytest's captured stdin is neither a tty nor
    # readable, so pretend it is a tty to skip that read entirely
    monkeypatch.setattr(
        dynamic_node_parser.sys.stdin, "isatty", lambda: True
    )


# pytest  ######################################################################
class TestDynamicNodeMain:

    def test_uses_default_corpus_tree_preface_when_heading_authored(
        self, monkeypatch, capsys
    ):
        root = PromptCorpusNode("○", None, [])
        AbbrGroupNode(
            root,
            group_name="some-group",
            preface=["This is the authored preface line."],
        )

        monkeypatch.setattr(
            dynamic_node_parser, "get_default_corpus_tree", lambda: root
        )

        parser = _build_dn_parser()
        args = parser.parse_args(["dynamic-node", "some-group"])
        args.func(args)

        out = capsys.readouterr().out
        assert "This is the authored preface line." in out

    def test_falls_back_to_empty_tree_when_no_default_corpus_tree(
        self, monkeypatch, capsys
    ):
        def _raise_no_default():
            raise ValueError("no default corpus tree set")

        monkeypatch.setattr(
            dynamic_node_parser, "get_default_corpus_tree", _raise_no_default
        )

        parser = _build_dn_parser()
        args = parser.parse_args(["dynamic-node", "today"])
        args.func(args)

        out = capsys.readouterr().out
        assert out.strip() != ""

    def test_falls_back_when_heading_not_authored_in_default_tree(
        self, monkeypatch, capsys
    ):
        root = PromptCorpusNode("○", None, [])

        monkeypatch.setattr(
            dynamic_node_parser, "get_default_corpus_tree", lambda: root
        )

        parser = _build_dn_parser()
        args = parser.parse_args(["dynamic-node", "some-group"])
        args.func(args)

        out = capsys.readouterr().out
        assert "This is the authored preface line." not in out
