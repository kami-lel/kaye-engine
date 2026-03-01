"""
api-commit-primary_test.py

Unit Tests (using pytest) for:

/kaye/dify-ap/kaye-commit-sense/primary-message
"""

import pytest


@pytest.fixture
def endpoint(app_endpoint):
    return app_endpoint + "/primary_message"


# TODO unit tests
