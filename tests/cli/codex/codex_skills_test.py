"""
tests/cli/codex/codex_skills_test.py

test: ``codex skills`` -- every exportable as a skill folder, the ``s``
alias, the personal default folder
"""

from argparse import ArgumentParser

from kaye_engine.cli.codex.main import register_cli_codex_parser
from kaye_engine.cli.codex.skills import parser as skills_parser

from tests.cli.codex.codex_plugin_test import two_consumers  # noqa: F401


class TestStructure:

    def test_skills_aliases(_):
        root = ArgumentParser()
        register_cli_codex_parser(root.add_subparsers())

        for argv in (["codex", "skills"], ["o", "s"]):
            assert callable(root.parse_args(argv).func)

    def test_default_folder_is_agents_skills(_):
        folder = skills_parser.DEFAULT_CODEX_SKILLS_FOLDER
        assert folder.parts[-2:] == (".agents", "skills")


class TestContent:

    def test_writes_every_exportable_as_skill(
        _, two_consumers, tmp_path  # noqa: F811
    ):
        root = ArgumentParser()
        register_cli_codex_parser(root.add_subparsers())
        args = root.parse_args(["o", "s", str(tmp_path)])

        args.func(args)

        assert sorted(p.name for p in tmp_path.iterdir()) == [
            "one-skill",
            "two-skill",
        ]
        assert (tmp_path / "one-skill" / "SKILL.md").is_file()
