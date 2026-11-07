"""
verbosity_test.py

Unit Tests (using pytest) for:

apply_verbosity_arg
"""

import logging
from argparse import ArgumentParser

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


@pytest.fixture(autouse=True)
def restore_levels():
    saved = {n: kamilog.getLogger(n).level for n in _LOGGER_NAMES}
    yield
    for name, level in saved.items():
        kamilog.getLogger(name).setLevel(level)


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
