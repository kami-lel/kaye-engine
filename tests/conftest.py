"""
tests/conftest.py

register every abbr glossary name used across the test suite; module-level
so it runs at collection time, before any test module (some of which
build ``AbbrData`` at class-body scope) is imported
"""

from tests.consumer_helper import ensure_test_consumer, register_abbr_glossary

ensure_test_consumer()

for _glossary_name in (
    "coding-terms",
    "programming-language-codes",
    "natural-language-codes",
    "usable-abbreviations",
    "unity-engine-abbr",
    "plan-step-by-step-abbr",
    "code-documentation-field-abbr",
    "other-glossary",
    "g",
):
    register_abbr_glossary(_glossary_name, True)

register_abbr_glossary(
    "some-glossary", True, is_dyn_substitution=True
)
