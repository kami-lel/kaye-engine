"""
tests/cli/hermes/parser_test.py

Unit Tests (using pytest) for:

register_hermes_parser
"""

from argparse import ArgumentParser
from unittest.mock import patch

import pytest

from kaye_engine.cli.hermes import parser


# auxiliaries  #################################################################
def _build_parser():
    root_parser = ArgumentParser()
    subparser = root_parser.add_subparsers()
    parser.register_hermes_parser(subparser)
    return root_parser


@pytest.fixture(autouse=True)
def _no_corpus_setup_guard():
    with patch.object(parser, "check_corpus_setup_for_cli", lambda: None):
        with patch.object(
            parser, "get_consumer_version", lambda: "1.0"
        ):
            yield


# pytest  ######################################################################
class TestRegisterHermesParser:

    @pytest.mark.parametrize("name", ["hermes", "m"])
    def test_name_and_alias(_, name, tmp_path):
        args = _build_parser().parse_args([name, str(tmp_path)])

        assert callable(args.func)

    def test_folder_is_required(_):
        with pytest.raises(SystemExit):
            _build_parser().parse_args(["hermes"])

    def test_render_flags_present(_, tmp_path):
        args = _build_parser().parse_args(
            ["hermes", str(tmp_path), "--variant", "V", "--sparseness", "0"]
        )

        assert list(args.variant) == ["V"]


class TestHermesMain:

    def test_passes_folder_version_and_render_profile(_, tmp_path):
        args = _build_parser().parse_args(["m", str(tmp_path)])

        with patch.object(parser, "export_hermes_folder") as export:
            args.func(args)

        export.assert_called_once()
        assert export.call_args.args == (tmp_path,)
        assert export.call_args.kwargs["version"] == "1.0"
        assert export.call_args.kwargs["render_profile"] is not None

    def test_dry_run_flag_parses(_, tmp_path):
        args = _build_parser().parse_args(["m", str(tmp_path), "-n"])

        assert args.dry_run is True
