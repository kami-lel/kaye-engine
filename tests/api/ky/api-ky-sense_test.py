"""
api-dify-ky-sense_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense
"""


# helpers  #####################################################################
def _assert_start_opt(opt):
    assert opt.startswith("""# Kaye Chat
## sense
In the JSON output, **always** use the defaults below; **change a value only** when the instructions include a **clearly labeled, field-specific section** that explicitly sets that same field:

- `programming_languages`: `""`
- `role`: `""`
- `llm`: `""`
- `difficulty`: `0`""")


def _assert_llm_opt(opt):
    assert (
        """### llm
choose exactly one label that best matches the **difficulty and reasoning complexity** required to answer the user's request (not the topic or length). base your choice on how many dependent steps, judgments, or non-trivial inferences are needed to produce a correct answer.

- `rapid`: least complex. highly mechanical, immediate tasks with virtually no reasoning or judgment (reformatting, converting, extracting, renaming, simple templating).
- `chat`: low complexity. straightforward conversational answers from broad knowledge with minimal reasoning (definitions, simple explanations, basic factual Q&A).
- `think`: medium complexity. requires multiple connected steps and some judgment (planning, troubleshooting, comparing options against criteria, structured step-by-step help).
- `think-think`: highest complexity. requires deep/extended reasoning, creative synthesis, or balancing constraints and trade-offs across many steps (system design, novel strategies, complex multi-constraint problem solving)."""
        in opt
    )


def _assert_role_opt(opt):
    assert (
        """### role
select exactly one role. pick the role that matches the **main type of work** the user wants.

- `rapid`: do quick, repetitive, *mechanical* tasks with almost no reasoning (direct text transformations, simple conversions, basic reformatting).
- `chat`: do general conversation and simple information Q&A (the request is not mainly a transformation and not mainly coding).
- `coder`: help with programming tasks (write, expand, or edit code; debug; explain code; reason about implementation details)
- `barista`: manage coffee notes (record brews, organize tasting notes)
- `changelog`: write and format changelogs (draft entries, normalize wording)"""
        in opt
    )


def _assert_empty_opt(opt):
    assert """### leave empty
`programming_languages` must be empty string
`difficulty` must be `0`""" in opt


class TestNoRole:  #############################################################

    def test1(self, flask_test_client, sense_endpoint):
        response = flask_test_client.get(sense_endpoint)
        opt = response.get_data().decode("utf-8")

        print(opt)

        _assert_start_opt(opt)
        _assert_llm_opt(opt)
        _assert_role_opt(opt)
        _assert_empty_opt(opt)

    def test2(self, flask_test_client, sense_endpoint):
        response = flask_test_client.get(
            sense_endpoint, query_string={"role": ""}
        )
        opt = response.get_data().decode("utf-8")

        print(opt)

        _assert_start_opt(opt)
        _assert_llm_opt(opt)
        _assert_role_opt(opt)
        _assert_empty_opt(opt)


class TestRoleCoder:  ##########################################################

    # tests  ===================================================================
    def test1(self, flask_test_client, sense_endpoint):
        response = flask_test_client.get(
            sense_endpoint, query_string={"role": "coder"}
        )
        opt = response.get_data().decode("utf-8")

        print(opt)

        _assert_start_opt(opt)

        assert opt.endswith(
            """- `0.90` Add observability (structured logs, metrics, tracing) with request IDs end-to-end.
- `0.98` Implement an advanced distributed algorithm prototype (e.g., Raft leader election).
- `0.99` Build a small interpreter/compiler (lexer → parser → AST → evaluator) with tests.
- `1.00` Start a monolith→microservices migration: plan + implement first extraction safely.
"""
        )
        assert "#### programming_languages" in opt
        assert "##### Programming Languages Code" in opt
        assert "#### difficulty" in opt


class TestOtherRole:  ##########################################################

    def test_other_role(self, flask_test_client, sense_endpoint):
        response = flask_test_client.get(
            sense_endpoint, query_string={"role": "aaa"}
        )
        opt = response.get_data().decode("utf-8")

        print(opt)

        _assert_start_opt(opt)
        _assert_llm_opt(opt)
        _assert_empty_opt(opt)
