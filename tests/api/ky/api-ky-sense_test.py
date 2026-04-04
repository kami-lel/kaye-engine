"""
api-dify-ky-sense_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/ky/sense
"""

# helpers  #####################################################################

# Pytest unit tests  ###########################################################


class TestDefault:  # ==========================================================

    def test_both_default(_, flask_test_client, sense_endpoint):
        pass

    def test_both_empty(_, flask_test_client, sense_endpoint):
        pass

    def test_both_missing(_, flask_test_client, sense_endpoint):
        response = flask_test_client.post(sense_endpoint)
        opt = response.get_data().decode("utf-8")

        print(opt)
        assert False  # HACK HACK


# HACK #####################################################################


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
select exactly one role. choose the role that best matches the *kind of input* the user gives you. prefer the **most specific** matching role.

- `rapid`: when the user gives you content that needs a **simple mechanical change** with little judgment, such as reformatting, extracting, sorting, converting, cleaning, splitting, merging, or applying a narrow rule to existing text or data
- `chat`: when the user gives you a **general question or everyday request** and no more specific role clearly applies
- `coder`: when the user gives you **code or software-related material**, such as source code, error messages, technical requirements, scripts, configuration, debugging questions, or implementation problems
- `barista`: when the user gives you **coffee-related information**, such as beans, origins, roast details, brew methods, ratios, grind settings, equipment, tasting notes, drink results, prices, or brewing logs"""
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

        assert (
            """- `0.93` Optimize a slow loop by reducing nested iterations or caching loop variables.
- `0.96` Integrate a standard third-party SDK for a straightforward feature; mock in tests.
- `0.98` Convert a sync flow to async/await (or equivalent) without behavior changes.
- `1.00` Refactor a messy module into smaller units without changing behavior; update tests."""
            in opt
        )

        assert "#### programming_languages" in opt
        assert "#### difficulty" in opt
        assert "# {Programming Languages Code}" in opt


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
