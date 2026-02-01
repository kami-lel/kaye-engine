"""
prompt_abbr_load_test.py

Unit Tests (using pytest) for:

- load_abbrs_json()
"""

from kaye.gen_prompt import DynamicAbbrBlueprint


def test_aaa():
    # HACK
    DynamicAbbrBlueprint.load_abbrs_json()
