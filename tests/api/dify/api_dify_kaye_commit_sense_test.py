"""
api_dify_kaye_commit_sense_test.py

Unit Tests (using pytest) for: /kaye/dify-app/kaye-commit-sense/*
"""

from kaye.gen_prompt import load_embedded_prompt_corpus, PromptBlueprint

APP_PREFIX = "/kaye/dify-app/kaye-commit-sense"


# prompt parts  ################################################################


COMMENT_BRIEFNESS = PromptBlueprint.parse(
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

YES_MD = PromptBlueprint.parse(
    load_embedded_prompt_corpus(),
    """ ○
[x] └── Format
""",
).generate_prompt(hide_comment=True)

NO_MD = PromptBlueprint.parse(
    load_embedded_prompt_corpus(),
    """ ○
[ ] └── Role
[ ]     └── Kaye Commit Sense
[x]         └── no markdown syntax
""",
).generate_prompt(hide_comment=True)


AM = PromptBlueprint.parse(
    load_embedded_prompt_corpus(),
    """ ○
[ ] ├── Elements
[x] │   └── Annotation Markers
[ ] ├── Style
[ ] │   ├── Capitalization Style
[ ] │   │   └── Commentary Case
[ ] │   └── Briefness Style
[ ] └── Role
[ ]     └── Kaye Commit Sense
[ ]         └── Per File Summary Task
[ ]             └── Prefix Symbol
[ ]                 └── Long
""",
).generate_prompt(hide_comment=True)


COMMIT_SENSE = PromptBlueprint.parse(
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


PER_FILE_SUMMARY_TASK = PromptBlueprint.parse(
    load_embedded_prompt_corpus(),
    """   ○
[ ] ├── Elements
[ ] │   └── Annotation Markers
[ ] ├── Style
[ ] │   ├── Capitalization Style
[ ] │   │   └── Commentary Case
[ ] │   └── Briefness Style
[ ] └── Role
[ ]     └── Kaye Commit Sense
[x]         └── Per File Summary Task
[x]             └── Prefix Symbol
""",
).generate_prompt(hide_comment=True)


class TestPrimary:  # /primary-message  ########################################

    url = APP_PREFIX + "/primary-message"

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
        response = flask_test_client.get(self.url)

        opt = response.data.decode("utf-8")
        print(opt)

        assert COMMENT_BRIEFNESS in opt
        assert COMMIT_SENSE in opt
        assert self.part3 in opt

    # param allows_md  ---------------------------------------------------------
    def test_md_empty(self, flask_test_client):
        params = "?allows_md="
        response = flask_test_client.get(self.url + params)

        opt = response.data.decode("utf-8")
        print(opt)

        assert COMMENT_BRIEFNESS in opt
        assert COMMIT_SENSE in opt
        assert self.part3 in opt

        assert NO_MD in opt

    def test_md_0(self, flask_test_client):
        params = "?allows_md=0"
        response = flask_test_client.get(self.url + params)

        opt = response.data.decode("utf-8")
        print(opt)

        assert COMMENT_BRIEFNESS in opt
        assert COMMIT_SENSE in opt
        assert self.part3 in opt

        assert NO_MD in opt

    def test_md_1(self, flask_test_client):  # BUG
        params = "?allows_md=1"
        response = flask_test_client.get(self.url + params)

        opt = response.data.decode("utf-8")
        print(opt)

        assert COMMENT_BRIEFNESS in opt
        assert COMMIT_SENSE in opt
        assert self.part3 in opt

        assert YES_MD in opt

    def test_md_bad_type(self, flask_test_client):
        pass  # TODO

    def test_md_bad_value(self, flask_test_client):
        pass  # TODO


class TestLong:  # /per-file-long  #############################################

    url = APP_PREFIX + "/per-file-long"
    distinct = PromptBlueprint.parse(
        load_embedded_prompt_corpus(),
        """ ○
    [ ] ├── Elements
    [ ] │   └── Annotation Markers
    [ ] ├── Style
    [ ] │   ├── Capitalization Style
    [ ] │   │   └── Commentary Case
    [ ] │   └── Briefness Style
    [ ] └── Role
    [ ]     └── Kaye Commit Sense
    [ ]         └── Per File Summary Task
    [ ]             └── Prefix Symbol
    [x]                 └── Long
    """,
    ).generate_prompt(hide_comment=True)

    def test_fx(self, flask_test_client):
        response = flask_test_client.get(self.url)

        opt = response.data.decode("utf-8")
        print(opt)

        assert AM in opt
        assert COMMENT_BRIEFNESS in opt
        assert COMMIT_SENSE in opt
        assert PER_FILE_SUMMARY_TASK in opt
        assert self.distinct in opt

    # param allows_md  ---------------------------------------------------------
    def test_md_0(self, flask_test_client):
        params = "?allows_md=0"
        response = flask_test_client.get(self.url + params)

        opt = response.data.decode("utf-8")
        print(opt)

        assert AM in opt
        assert COMMENT_BRIEFNESS in opt
        assert COMMIT_SENSE in opt
        assert PER_FILE_SUMMARY_TASK in opt
        assert self.distinct in opt

        assert NO_MD in opt

    def test_md_1(self, flask_test_client):  # BUG
        params = "?allows_md=1"
        response = flask_test_client.get(self.url + params)

        opt = response.data.decode("utf-8")
        print(opt)

        assert AM in opt
        assert COMMENT_BRIEFNESS in opt
        assert COMMIT_SENSE in opt
        assert PER_FILE_SUMMARY_TASK in opt
        assert self.distinct in opt

        assert YES_MD in opt


class TestShort:  # /per-file-short  ###########################################

    url = APP_PREFIX + "/per-file-short"
    distinct = PromptBlueprint.parse(
        load_embedded_prompt_corpus(),
        """ ○
    [ ] ├── Elements
    [ ] │   └── Annotation Markers
    [ ] ├── Style
    [ ] │   ├── Capitalization Style
    [ ] │   │   └── Commentary Case
    [ ] │   └── Briefness Style
    [ ] └── Role
    [ ]     └── Kaye Commit Sense
    [ ]         └── Per File Summary Task
    [ ]             └── Prefix Symbol
    [x]                 └── Short
    """,
    ).generate_prompt(hide_comment=True)

    def test_fx(self, flask_test_client):
        response = flask_test_client.get(self.url)

        opt = response.data.decode("utf-8")
        print(opt)

        assert AM in opt
        assert COMMENT_BRIEFNESS in opt
        assert COMMIT_SENSE in opt
        assert PER_FILE_SUMMARY_TASK in opt
        assert self.distinct in opt

    # param allows_md  ---------------------------------------------------------
    def test_md_0(self, flask_test_client):
        params = "?allows_md=0"
        response = flask_test_client.get(self.url + params)

        opt = response.data.decode("utf-8")
        print(opt)

        assert AM in opt
        assert COMMENT_BRIEFNESS in opt
        assert COMMIT_SENSE in opt
        assert PER_FILE_SUMMARY_TASK in opt
        assert self.distinct in opt

        assert NO_MD in opt

    def test_md_1(self, flask_test_client):  # BUG
        params = "?allows_md=1"
        response = flask_test_client.get(self.url + params)

        opt = response.data.decode("utf-8")
        print(opt)

        assert AM in opt
        assert COMMENT_BRIEFNESS in opt
        assert COMMIT_SENSE in opt
        assert PER_FILE_SUMMARY_TASK in opt
        assert self.distinct in opt

        assert YES_MD in opt
