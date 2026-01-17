"""
api_dify_kaye_commit_sense_test.py

Unit Tests (using pytest) for: /kaye/dify-app/kaye-commit-sense/*
"""

from kaye.gen_prompt import load_embedded_prompt_corpus, PromptBlueprint
from api.dify_app.kaye_commit_sense import (
    PRIMARY_MESSAGE_PROMPT_BLUEPRINT,
    PER_FILE_LONG_PROMPT_BLUEPRINT,
    PER_FILE_SHORT_PROMPT_BLUEPRINT,
)

APP_PREFIX = "/kaye/dify-app/kaye-commit-sense"


class TestPrimary:  # /primary-message  ########################################

    part1 = PromptBlueprint.parse(
        load_embedded_prompt_corpus(),
        """ ○
[ ] ├── Style
[ ] │   ├── Capitalization Style
[x] │   │   └── Commentary Case
[x] │   └── Briefness Style
[ ] └── Role
[ ]     └── Kaye Commit Sense
[ ]         └── Primary Message Task
""",
    ).generate_prompt(hide_comment=True)

    part2 = PromptBlueprint.parse(
        load_embedded_prompt_corpus(),
        """ ○
[ ] ├── Style
[ ] │   ├── Capitalization Style
[ ] │   │   └── Commentary Case
[ ] │   └── Briefness Style
[ ] └── Role
[x]     └── Kaye Commit Sense
[ ]         └── Primary Message Task
""",
    ).generate_prompt(hide_comment=True)

    part3 = PromptBlueprint.parse(
        load_embedded_prompt_corpus(),
        """ ○
[ ] ├── Style
[ ] │   ├── Capitalization Style
[ ] │   │   └── Commentary Case
[ ] │   └── Briefness Style
[ ] └── Role
[ ]     └── Kaye Commit Sense
[x]         └── Primary Message Task
""",
    ).generate_prompt(hide_comment=True)

    def test_fx(self, flask_test_client):
        response = flask_test_client.get(APP_PREFIX + "/primary-message")

        opt = response.data.decode("utf-8")
        print(opt)

        assert self.part1 in opt
        assert self.part2 in opt
        assert self.part3 in opt


class TestLong:  # /per-file-long  #############################################

    def test_fx(_, flask_test_client):
        response = flask_test_client.get(APP_PREFIX + "/per-file-long")

        opt = response.data.decode("utf-8")
        print(opt)

        assert (
            opt
            == PromptBlueprint.parse(
                load_embedded_prompt_corpus(), PER_FILE_LONG_PROMPT_BLUEPRINT
            ).generate_prompt()
        )


class TestShort:  # /per-file-short  ###########################################

    def test_fx(_, flask_test_client):
        response = flask_test_client.get(APP_PREFIX + "/per-file-short")

        opt = response.data.decode("utf-8")
        print(opt)

        assert (
            opt
            == PromptBlueprint.parse(
                load_embedded_prompt_corpus(), PER_FILE_SHORT_PROMPT_BLUEPRINT
            ).generate_prompt()
        )


# TODO tests for params
