"""
prompt_abbr_gen_test.py

Unit Tests (using pytest) for:

DynamicAbbrBlueprint._generate_abbr_content()
"""

from kaye.gen_prompt import AbbrNode

# TODO TODO


def test_tmp():  # HACK
    AbbrNode.load_abbrs_json()
    a = AbbrNode._automaton

    t = """this is some Text w/ abbr that"""

    for v in a.iter(t):
        print(v)

    assert False
