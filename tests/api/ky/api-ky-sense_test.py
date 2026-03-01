"""
api-dify-ky-sense_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense
"""


class TestNoRole:  #############################################################

    answer_start ="""# Kaye Chat
## sense
In the JSON output, **always** use the defaults below; **change a value only** when the instructions include a **clearly labeled, field-specific section** that explicitly sets that same field:

- `programming_languages`: `""`
- `role`: `""`
- `llm`: `""`
- `difficulty`: `0`"""


    answer_end = """- `think-think`: queries that require deep, abstract, or prolonged reasoning, creative synthesis, designing solutions with trade-offs, or tasks that need many chained logical steps.

### role
- `chat` for normal conversation
- `peer_coder` if user ask code related questions

### leave empty
`programming_languages` must be empty string
`difficulty` must be `0`
"""

    # tests  ===================================================================

    def test1(self, flask_test_client, sense_endpoint):
        response = flask_test_client.get(sense_endpoint)
        opt = response.get_data().decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)

    def test2(self, flask_test_client, sense_endpoint):
        response = flask_test_client.get(
            sense_endpoint, query_string={"role": ""}
        )
        opt = response.get_data().decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)


class TestRoleCoder:  ##########################################################

    # tests  ===================================================================
    def test1(self, flask_test_client, sense_endpoint):
        response = flask_test_client.get(
            sense_endpoint, query_string={"role": "peer_coder"}
        )
        opt = response.get_data().decode("utf-8")

        print(opt)
        assert opt.startswith("""# Kaye Chat
## sense
In the JSON output, **always** use the defaults below; **change a value only** when the instructions include a **clearly labeled, field-specific section** that explicitly sets that same field:

- `programming_languages`: `""`
- `role`: `""`
- `llm`: `""`
- `difficulty`: `0`""")
        assert opt.endswith("""- `0.90` Add observability (structured logs, metrics, tracing) with request IDs end-to-end.
- `0.98` Implement an advanced distributed algorithm prototype (e.g., Raft leader election).
- `0.99` Build a small interpreter/compiler (lexer → parser → AST → evaluator) with tests.
- `1.00` Start a monolith→microservices migration: plan + implement first extraction safely.
""")
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
        assert opt.startswith("""# Kaye Chat
## sense
In the JSON output, **always** use the defaults below;""")
        assert opt.endswith("""### leave empty
`programming_languages` must be empty string
`difficulty` must be `0`
""")
        assert """### llm
select the single most appropriate label to describe the nature of the user's query:""" \
                in opt