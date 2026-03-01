"""
api-commit-short_test.py

Unit Tests (using pytest) for:

/kaye/dify-ap/kaye-commit-sense/per-file-short
"""

import pytest


@pytest.fixture
def endpoint(app_endpoint):
    return app_endpoint + "/per-file-short"


# TODO unit tests
