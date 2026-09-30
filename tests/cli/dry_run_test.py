"""
dry_run_test.py

Unit Tests (using pytest) for:

build_dry_run_parent_parser, enable_dry_run, disable_dry_run, is_dry_run
"""

from argparse import ArgumentParser

import kamilog
import pytest

from kaye_engine.cli import dry_run
from kaye_engine.cli.dry_run import (
    build_dry_run_parent_parser,
    disable_dry_run,
    enable_dry_run,
    is_dry_run,
)


# auxiliaries  ##################################################################
@pytest.fixture(autouse=True)
def _reset_dry_run():
    disable_dry_run()
    yield
    disable_dry_run()


# TestParser  ####################################################################
class TestParser:
    @staticmethod
    def _parse(argv):
        parser = ArgumentParser(parents=[build_dry_run_parent_parser()])
        return parser.parse_args(argv)

    def test_default_is_live(_):
        assert _parse_default() is False

    def test_flag_sets_true(_):
        assert TestParser._parse(["--dry-run"]).dry_run is True

    def test_has_no_short_flag(_):
        with pytest.raises(SystemExit):
            TestParser._parse(["-n"])

    def test_builds_fresh_parser_per_call(_):
        assert build_dry_run_parent_parser() is not build_dry_run_parent_parser()


def _parse_default():
    return TestParser._parse([]).dry_run


# TestSwitch  ####################################################################
class TestSwitch:
    def test_starts_live(_):
        assert is_dry_run() is False

    def test_enable_turns_on(_):
        enable_dry_run()
        assert is_dry_run() is True

    def test_disable_turns_off(_):
        enable_dry_run()
        disable_dry_run()
        assert is_dry_run() is False

    @pytest.mark.parametrize("name", dry_run._LOGGER_NAMES)
    def test_enable_badges_every_engine_logger(_, name):
        enable_dry_run()
        assert kamilog.getLogger(name)._run_badges == (dry_run.DRY_BADGE,)

    @pytest.mark.parametrize("name", dry_run._LOGGER_NAMES)
    def test_disable_clears_every_engine_logger(_, name):
        enable_dry_run()
        disable_dry_run()
        assert kamilog.getLogger(name)._run_badges == ()
