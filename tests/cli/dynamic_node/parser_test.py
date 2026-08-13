"""
tests/cli/dynamic_node/parser_test.py

Unit Tests (using pytest) for:

_dynamic_node_main, register_dynamic_node_parser
"""

from argparse import ArgumentParser

import pytest

from kaye_engine.abbr_collection import AbbrData, AbbrMeaning
from kaye_engine.cli.dynamic_node import parser as dynamic_node_parser
from kaye_engine.prompt.dynamic_nodes import GlossaryNode, TodayNode
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
        GlossaryNode(
            root,
            glossary_name="some-glossary",
            preface=["This is the authored preface line."],
        )

        monkeypatch.setattr(
            dynamic_node_parser, "get_default_corpus_tree", lambda: root
        )

        parser = _build_dn_parser()
        args = parser.parse_args(["dynamic-node", "some-glossary"])
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

    def test_reuses_authored_engine_defined_node_without_duplicating(
        self, monkeypatch, capsys
    ):
        # regression: TodayNode.HEADING == "Today", but the CLI's NODE
        # key for it is the lowercase "today" -- matching the authored
        # "(...)" heading by the raw NODE arg instead of by HEADING used
        # to falsely conclude no authored heading existed, so a second
        # TodayNode got attached alongside the real one and both rendered
        root = PromptCorpusNode("○", None, [])
        TodayNode(root, preface=["This is the authored Today preface."])

        monkeypatch.setattr(
            dynamic_node_parser, "get_default_corpus_tree", lambda: root
        )

        parser = _build_dn_parser()
        args = parser.parse_args(["dynamic-node", "today"])
        args.func(args)

        out = capsys.readouterr().out
        assert out.count("(Today)") == 1
        assert "This is the authored Today preface." in out

    def test_falls_back_when_heading_not_authored_in_default_tree(
        self, monkeypatch, capsys
    ):
        root = PromptCorpusNode("○", None, [])

        monkeypatch.setattr(
            dynamic_node_parser, "get_default_corpus_tree", lambda: root
        )

        parser = _build_dn_parser()
        args = parser.parse_args(["dynamic-node", "some-glossary"])
        args.func(args)

        out = capsys.readouterr().out
        assert "This is the authored preface line." not in out


class TestPriorityThresholdFlag:  ##############################################

    @pytest.fixture(autouse=True)
    def _no_default_corpus_tree(self, monkeypatch):
        def _raise_no_default():
            raise ValueError("no default corpus tree set")

        monkeypatch.setattr(
            dynamic_node_parser, "get_default_corpus_tree", _raise_no_default
        )

    @pytest.fixture
    def _abbr_data(self, monkeypatch):
        data = AbbrData()
        with data:
            data.add_entry(
                AbbrMeaning("for example"),
                "e.g.",
                {
                    "priority": 1,
                    "tags": ["some-glossary"],
                    "wrap": "word",
                },
            )
            data.add_entry(
                AbbrMeaning("id est"),
                "i.e.",
                {
                    "priority": 6,
                    "tags": ["some-glossary"],
                    "wrap": "word",
                },
            )

        monkeypatch.setattr(
            "kaye_engine.prompt.dynamic_nodes.glossary_node.get_abbr_data",
            lambda: data,
        )
        return data

    def test_filters_by_threshold(self, _abbr_data, capsys):
        parser = _build_dn_parser()
        args = parser.parse_args(
            ["dynamic-node", "some-glossary", "-t", "5"]
        )
        args.func(args)

        out = capsys.readouterr().out
        assert "e.g.:for example" in out
        assert "i.e.:id est" not in out

    def test_omitted_renders_all(self, _abbr_data, capsys):
        parser = _build_dn_parser()
        args = parser.parse_args(["dynamic-node", "some-glossary"])
        args.func(args)

        out = capsys.readouterr().out
        assert "e.g.:for example" in out
        assert "i.e.:id est" in out


class TestMultipleNodes:  ######################################################

    def test_renders_every_given_node_in_one_merged_output(
        self, monkeypatch, capsys
    ):
        root = PromptCorpusNode("○", None, [])
        GlossaryNode(
            root,
            glossary_name="some-glossary",
            preface=["This is the some-glossary preface line."],
        )

        monkeypatch.setattr(
            dynamic_node_parser, "get_default_corpus_tree", lambda: root
        )

        parser = _build_dn_parser()
        args = parser.parse_args(
            ["dynamic-node", "some-glossary", "today"]
        )
        args.func(args)

        out = capsys.readouterr().out
        assert "This is the some-glossary preface line." in out
        assert "Today" in out

    def test_renders_two_glossaries_sharing_one_corpus_tree(
        self, monkeypatch, capsys
    ):
        root = PromptCorpusNode("○", None, [])
        GlossaryNode(
            root,
            glossary_name="some-glossary",
            preface=["This is the some-glossary preface line."],
        )
        GlossaryNode(
            root,
            glossary_name="other-glossary",
            preface=["This is the other-glossary preface line."],
        )

        monkeypatch.setattr(
            dynamic_node_parser, "get_default_corpus_tree", lambda: root
        )

        parser = _build_dn_parser()
        args = parser.parse_args(
            ["dynamic-node", "some-glossary", "other-glossary"]
        )
        args.func(args)

        out = capsys.readouterr().out
        assert "This is the some-glossary preface line." in out
        assert "This is the other-glossary preface line." in out

    def test_ls_combined_with_other_nodes_errors(self, capsys):
        parser = _build_dn_parser()
        args = parser.parse_args(["dynamic-node", "ls", "today"])

        with pytest.raises(SystemExit):
            args.func(args)


class TestSparsenessFlag:  #####################################################

    @pytest.fixture(autouse=True)
    def _two_glossaries(self, monkeypatch):
        root = PromptCorpusNode("○", None, [])
        GlossaryNode(
            root,
            glossary_name="some-glossary",
            preface=["This is the some-glossary preface line."],
        )
        GlossaryNode(
            root,
            glossary_name="other-glossary",
            preface=["This is the other-glossary preface line."],
        )

        monkeypatch.setattr(
            dynamic_node_parser, "get_default_corpus_tree", lambda: root
        )

    def test_omitted_defaults_to_no_blank_lines(self, capsys):
        parser = _build_dn_parser()
        args = parser.parse_args(
            ["dynamic-node", "some-glossary", "other-glossary"]
        )
        args.func(args)

        out = capsys.readouterr().out
        assert "\n\n" not in out
        assert "This is the some-glossary preface line." in out
        assert "This is the other-glossary preface line." in out

    def test_zero_removes_blank_lines(self, capsys):
        parser = _build_dn_parser()
        args = parser.parse_args(
            ["dynamic-node", "some-glossary", "other-glossary", "-s", "0"]
        )
        args.func(args)

        out = capsys.readouterr().out
        assert "\n\n" not in out
        assert "This is the some-glossary preface line." in out
        assert "This is the other-glossary preface line." in out

    def test_negative_one_collapses_to_single_line(self, capsys):
        parser = _build_dn_parser()
        args = parser.parse_args(
            ["dynamic-node", "some-glossary", "other-glossary", "-s", "-1"]
        )
        args.func(args)

        out = capsys.readouterr().out
        assert "\n" not in out.rstrip("\n")

    def test_accepts_none_literal(self):
        # ``_sparseness_type`` maps the literal "none" to ``None`` -- the
        # underlying ``_apply_sparseness()`` (render.py) does not itself
        # support a ``None`` policy, matching prompt generate's existing
        # pre-existing "none" flag behavior; this only covers CLI parsing
        parser = _build_dn_parser()
        args = parser.parse_args(
            ["dynamic-node", "some-glossary", "-s", "none"]
        )

        assert args.sparseness is None
