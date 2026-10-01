"""
tests/cli/blueprint/conftest.py

shared fixtures: a loaded corpus, registered blueprints, a parser built
the way the real CLI builds it, and a fake stdin
"""

import io
import logging
from argparse import ArgumentParser

import pytest

from kaye_engine import LOGGER_NAME
from kaye_engine.cli.blueprint.main_parser import register_cli_blueprint_parser
from kaye_engine.prompt.blueprint import (
    Blueprint,
    blueprint_registry,
    register_blueprint,
)
from kaye_engine.prompt.prompt_corpus_loader import (
    clear_corpus_tree,
    load_corpus_tree,
)

CORPUS = """# Project
Overview text.
## Install
Clone it.
### {note}
Noted text.
## License
MIT.
"""

PROJECT = ("Project",)
INSTALL = ("Project", "Install")
LICENSE = ("Project", "License")


class FakeStdin(io.StringIO):
    def __init__(self, text="", *, is_tty=False):
        super().__init__(text)
        self._is_tty = is_tty

    def isatty(self):
        return self._is_tty


@pytest.fixture(autouse=True)
def keep_logger_state():
    """the commands set the engine logger's level; undo it for later tests"""
    logger = logging.getLogger(LOGGER_NAME)
    level, propagate = logger.level, logger.propagate
    yield
    logger.setLevel(level)
    logger.propagate = propagate


@pytest.fixture
def corpus():
    clear_corpus_tree()
    load_corpus_tree([CORPUS])
    yield
    clear_corpus_tree()


@pytest.fixture
def registered(corpus):
    names = []

    def _register(name, blueprint, display_name="Display Name", **kwargs):
        register_blueprint(
            name, display_name, blueprint, is_exportable=False, **kwargs
        )
        names.append(name)

    _register(
        "test-cli-base", Blueprint(nodes=frozenset({PROJECT, INSTALL}))
    )
    _register(
        "test-cli-top",
        Blueprint(
            nodes=frozenset({LICENSE}), dependencies=("test-cli-base",)
        ),
    )

    yield _register

    for name in names:
        blueprint_registry.pop(name, None)


@pytest.fixture
def run(registered, monkeypatch, capsys):
    """run ``kaye-engine blueprint ARGV...``; returns ``(exit_code, out)``"""

    def _run(argv, *, stdin=None):
        parser = ArgumentParser()
        register_cli_blueprint_parser(parser.add_subparsers())
        monkeypatch.setattr("sys.stdin", FakeStdin(stdin or ""))
        capsys.readouterr()

        args = parser.parse_args(["blueprint", *argv])
        try:
            args.func(args)
            exit_code = 0
        except SystemExit as err:
            exit_code = err.code

        return exit_code, capsys.readouterr().out

    return _run
