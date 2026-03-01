"""
api-dify-ky-sense_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense
"""


class TestNoRole:  #############################################################

    answer_start = """# Kaye Chat
## sense
### llm
select the single most appropriate label to describe the nature of the user's query:

- `rapid`: short, immediate, or highly repetitive tasks that require little or no reasoning;"""

    answer_end = """
- `peer_coder` if user ask code related questions

### leave empty
`programming_languages` must be empty
`difficulty` must be `0`
"""

    # tests  ===================================================================

    def test1(self, flask_test_client, sense_endpoint):
        response = flask_test_client.get(sense_endpoint)
        opt = response.data.decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)

    def test2(self, flask_test_client, sense_endpoint):
        response = flask_test_client.get(
            sense_endpoint, query_string={"role": ""}
        )
        opt = response.data.decode("utf-8")

        print(opt)
        assert opt.startswith(self.answer_start)
        assert opt.endswith(self.answer_end)


class TestRoleCoder:  ##########################################################

    # tests  ===================================================================
    def test1(self, flask_test_client, sense_endpoint):
        response = flask_test_client.get(
            sense_endpoint, query_string={"role": "peer_coder"}
        )
        opt = response.data.decode("utf-8")

        print(opt)
        assert opt.startswith("""# Kaye Chat
## sense
### for coder
`role` and `llm` must be empty""")
        assert opt.endswith("""
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
        opt = response.data.decode("utf-8")

        print(opt)
        assert opt.startswith(
            """# Kaye Chat
## sense
### llm
select the single most appropriate label to describe the nature of the user's query:"""
        )
        assert opt.endswith(
            """- `think-think`: queries that require deep, abstract, or prolonged reasoning, creative synthesis, designing solutions with trade-offs, or tasks that need many chained logical steps.

### leave empty
`programming_languages` must be empty
`difficulty` must be `0`
"""
        )
