"""
tests/conftest.py

register every abbr glossary name used across the test suite; module-level
so it runs at collection time, before any test module (some of which
build ``AbbrData`` at class-body scope) is imported
"""

from kaye_engine.abbr_collection import register_abbr_glossary

for _glossary_name in (
    "coding-terms",
    "programming-language-codes",
    "natural-language-codes",
    "usable-abbreviations",
    "unity-engine-abbr",
    "plan-step-by-step-abbr",
    "code-documentation-field-abbr",
    "some-glossary",
    "other-glossary",
    "g",
):
    register_abbr_glossary(_glossary_name)
