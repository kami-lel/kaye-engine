"""
api-dify-ky-sense_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense
"""

# BUG


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
select the single most appropriate label to describe the nature of the user's query:

- `rapid`: short, immediate, or highly repetitive tasks that require little or no reasoning; fast direct transformations or simple format conversions.

- `chat`: general conversational questions or information requests that rely on broad knowledge but do not require multi-step problem solving.

- `think`: queries that require moderate reasoning or multi-step solutions, such as planning, debugging, comparing, or stepwise explanations.

- `think-think`: queries that require deep, abstract, or prolonged reasoning, creative synthesis, designing solutions with trade-offs, or tasks that need many chained logical steps."""
        in opt
    )


def _assert_role_opt(opt):
    assert (
        """### role
- `chat`: normal conversation
- `coder`: assist users with coding, such as code expansion, code adjustment, coding support, explanation & reasoning, & debug"""
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
