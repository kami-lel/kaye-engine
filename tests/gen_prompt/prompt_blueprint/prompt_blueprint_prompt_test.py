"""
test .generate_prompt() and __str__()
"""

from tests.gen_prompt.prompt_blueprint.testees import PROMPT1, PROMPT2


def _remove_last_line(text):
    return "\n".join(text.split("\n")[:-1])


# BUG tests
