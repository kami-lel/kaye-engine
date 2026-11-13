"""
flag_letter_test.py

Unit Tests (using pytest) for:

the project-wide short-letter table: every short flag of every command
means one long flag, except ``claude user-system-prompt`` ``-c``
"""

import argparse
import collections

import pytest

from kaye_engine.cli.cli_main import register_cli_main_parser

# the one documented clash: ``claude user-system-prompt -c`` is ``--coder``
_EXEMPT = {("-c", "--coder", "user-system-prompt")}


# auxiliaries  #################################################################
def _walk(parser, path, seen, out):
    """
    collect ``short letter -> {(long flag, path)}`` over the whole tree,
    each parser visited once, aliases included in the path
    """
    if id(parser) in seen:
        return
    seen.add(id(parser))

    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name, sub in action.choices.items():
                _walk(sub, path + (name,), seen, out)
            continue
        longs = [opt for opt in action.option_strings if opt.startswith("--")]
        shorts = [opt for opt in action.option_strings if len(opt) == 2]
        for short in shorts:
            long_ = longs[0] if longs else short
            out[short].add((long_, path[-1] if path else ""))


def _collect_letters():
    cli_parser, _ = register_cli_main_parser()
    out = collections.defaultdict(set)
    _walk(cli_parser, (), set(), out)
    return out


# pytest  ######################################################################
class TestShortLetters:

    def test_each_short_letter_means_one_long_flag(_):
        letters = _collect_letters()

        clashes = {}
        for short, pairs in letters.items():
            longs = {
                long_
                for long_, command in pairs
                if (short, long_, command) not in _EXEMPT
            }
            if len(longs) > 1:
                clashes[short] = sorted(longs)

        assert clashes == {}

    def test_documented_exception_is_still_there(_):
        letters = _collect_letters()

        assert ("--coder", "usp") in letters["-c"] or (
            "--coder",
            "user-system-prompt",
        ) in letters["-c"]

    @pytest.mark.parametrize(
        "argv",
        [
            ["var", "-F"],
            ["var", "-a", "^a"],
            ["plugin", "-N"],
            ["json", "-f", "out.json"],
        ],
    )
    def test_dropped_letters_are_rejected(_, argv):
        cli_parser, _ = register_cli_main_parser()

        with pytest.raises(SystemExit):
            cli_parser.parse_args(argv)

    @pytest.mark.parametrize(
        "argv",
        [
            ["var", "--flat"],
            ["var", "--affordance", "^a"],
            ["json", "--output-file", "out.json"],
        ],
    )
    def test_long_forms_still_parse(_, argv):
        cli_parser, _ = register_cli_main_parser()

        cli_parser.parse_args(argv)
