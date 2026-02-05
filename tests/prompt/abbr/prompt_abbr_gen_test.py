"""
prompt_abbr_gen_test.py

Unit Tests (using pytest) for:

DynamicAbbrBlueprint._generate_abbr_content()
"""

from kaye.gen_prompt import AbbrNode


def test_tmp():  # Hack
    t = """this is some Text w/ abbr that"""

    print(AbbrNode().gen(t))

    assert False
