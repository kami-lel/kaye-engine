"""
continue_parser_test.py

Unit Tests (using pytest) for:

register_continue_parser
"""

from argparse import ArgumentParser
from pathlib import Path
from unittest.mock import patch

import pytest

from kaye_engine.cli.continue_ai import parser


# auxiliaries  #################################################################
def _build_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    parser.register_continue_parser(subparser)
    return root_parser


@pytest.fixture(autouse=True)
def _no_corpus_setup_guard():
    with patch.object(parser, "check_corpus_setup_for_cli", lambda: None):
        yield


# pytest  ######################################################################
class TestRegisterContinueParser:

    @pytest.mark.parametrize("name", ["continue", "c"])
    def test_name_and_alias(_, name):
        args = _build_parser().parse_args([name])

        assert callable(args.func)

    def test_folder_dft(_):
        args = _build_parser().parse_args(["continue"])

        assert args.folder == Path.home() / ".continue"

    def test_folder_explicit(_, tmp_path):
        args = _build_parser().parse_args(["continue", str(tmp_path)])

        assert args.folder == tmp_path

    def test_render_flags_present(_):
        args = _build_parser().parse_args(
            ["continue", "--variant", "V", "--sparseness", "0"]
        )

        assert list(args.variant) == ["V"]


class TestContinueMain:

    def test_passes_folder_and_render_profile(_, tmp_path):
        args = _build_parser().parse_args(["continue", str(tmp_path)])

        with patch.object(parser, "export_continue_folder") as export:
            args.func(args)

        export.assert_called_once()
        assert export.call_args.args == (tmp_path,)
        assert export.call_args.kwargs["render_profile"] is not None

    def test_dft_folder_reaches_exporter(_):
        args = _build_parser().parse_args(["c"])

        with patch.object(parser, "export_continue_folder") as export:
            args.func(args)

        assert export.call_args.args == (Path.home() / ".continue",)
