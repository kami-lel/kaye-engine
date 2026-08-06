"""
tests/conftest.py

register every abbr group name used across the test suite; module-level
so it runs at collection time, before any test module (some of which
build ``AbbrData`` at class-body scope) is imported
"""

from kaye_engine.abbr_collection import register_abbr_group

for _group_name in (
    "coding-terms",
    "programming-language-codes",
    "natural-language-codes",
    "usable-abbreviations",
    "unity-engine-abbr",
    "plan-step-by-step-abbr",
    "code-documentation-field-abbr",
    "some-group",
    "g",
):
    register_abbr_group(_group_name)
