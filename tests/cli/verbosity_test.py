"""
verbosity_test.py

Unit Tests (using pytest) for:

apply_verbosity_arg
"""

import logging
from argparse import ArgumentParser

from unittest.mock import patch

import kamilog
import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.verbosity import apply_verbosity_arg
from kaye_engine.skill import LOGGER_SKILL_NAME

_LOGGER_NAMES = (LOGGER_NAME, LOGGER_CLAUDE_NAME, LOGGER_SKILL_NAME)


def _parse(*argv):
    parser = ArgumentParser()
    kamilog.add_verbose_arguments(parser)
    return parser.parse_args(argv)


class TestContent:
    @pytest.mark.parametrize(
        "argv, level",
        [
            ((), kamilog.DONE),
            (("-V",), kamilog.DEBUG),
            (("-Q",), kamilog.CRITICAL),
            (("-v",), kamilog.INFO),
            (("-q",), kamilog.WARNING),
        ],
    )
    def test_every_engine_logger_gets_level(self, argv, level):
        apply_verbosity_arg(_parse(*argv))
        for name in _LOGGER_NAMES:
            assert kamilog.getLogger(name).getEffectiveLevel() == level

    def test_overrides_explicit_child_level(self):
        kamilog.getLogger(LOGGER_SKILL_NAME).setLevel(logging.ERROR)
        apply_verbosity_arg(_parse("-V"))
        skill_logger = kamilog.getLogger(LOGGER_SKILL_NAME)
        assert skill_logger.isEnabledFor(kamilog.DEBUG)

    def test_later_created_logger_inherits(self):
        apply_verbosity_arg(_parse("-V"))
        late = kamilog.getLogger(LOGGER_NAME + ".late-created")
        assert late.isEnabledFor(kamilog.DEBUG)


class TestVsCodeCommand:
    def test_max_verbose_reaches_skill_logger(self):
        from kaye_engine.cli.claude.vs_code import parser as vs_code_parser

        parser = ArgumentParser()
        kamilog.add_verbose_arguments(parser)
        args = parser.parse_args(["-V"])

        with patch.object(
            vs_code_parser,
            "check_setup_for_claude_cli",
            side_effect=SystemExit(1),
        ):
            with pytest.raises(SystemExit):
                vs_code_parser._vs_code_main(args)

        skill_logger = kamilog.getLogger(LOGGER_SKILL_NAME)
        assert skill_logger.isEnabledFor(kamilog.DEBUG)
