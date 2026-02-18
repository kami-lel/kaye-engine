"""
api-dify-ky-pre_sense_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/pre-sense
"""

import pytest


# pytest fixtures  #############################################################
@pytest.fixture
def local_endpoint(app_endpoint):
    return app_endpoint + "/pre-sense"


class TestNoRole:  #############################################################

    answer_start = """# Kaye Chat
## pre-sense
### llm
For `llm` field, select the single most appropriate label to describe the nature of the user's query:

- `rapid`: short, immediate, or highly repetitive tasks that require little or no reasoning; fast direct transformations or simple format conversions."""

    answer_end = """

### role
For `role` field.
"""

    # tests  ===================================================================

    def test1(self, flask_test_client, local_endpoint):
        response = flask_test_client.get(local_endpoint)
        opt = response.data.decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)

    def test2(self, flask_test_client, local_endpoint):
        response = flask_test_client.get(
            local_endpoint, query_string={"role": ""}
        )
        opt = response.data.decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)


class TestRoleCoder:  ##########################################################

    answer_start = """# Kaye Chat
## pre-sense
### for coder
#### plcs
Return a string containing the abbreviations of the programming languages (as defined below) required by the user, separated by commas. For example, `'py,cpp'`. If the conversation does not mention any specific programming language, such as when discussing conceptual or general algorithms, return an empty string (`''`)."""

    answer_end = """
- ``0.88`` Dockerize the app (Dockerfile + compose) and document local run steps.
- ``0.89`` Set up CI (lint/test/build) with caching and artifacts.
- ``0.90`` Add observability (structured logs, metrics, tracing) with request IDs end-to-end.
- ``0.98`` Implement an advanced distributed algorithm prototype (e.g., Raft leader election).
- ``0.99`` Build a small interpreter/compiler (lexer → parser → AST → evaluator) with tests.
- ``1.00`` Start a monolith→microservices migration: plan + implement first extraction safely.
"""

    # tests  ===================================================================
    def test1(self, flask_test_client, local_endpoint):
        response = flask_test_client.get(
            local_endpoint, query_string={"role": "peer_coder"}
        )
        opt = response.data.decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)
        assert """##### Programming Languages Code""" in opt
        assert """#### difficulty""" in opt


class TestOtherRole:  ##########################################################

    answer_start = """# Kaye Chat
## pre-sense
### llm
For `llm` field, select the single most appropriate label to describe the nature of the user's query:

- `rapid`: short, immediate, or highly repetitive tasks that require little or no reasoning; fast direct transformations or simple format conversions.
"""

    answer_end = """- `think`: queries that require moderate reasoning or multi-step solutions, such as planning, debugging, comparing, or stepwise explanations.

- `think-think`: queries that require deep, abstract, or prolonged reasoning, creative synthesis, designing solutions with trade-offs, or tasks that need many chained logical steps.
"""

    # tests  ===================================================================
    def test_other_role(self, flask_test_client, local_endpoint):
        response = flask_test_client.get(
            local_endpoint, query_string={"role": "aaa"}
        )
        opt = response.data.decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)
