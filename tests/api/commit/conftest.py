import pytest


@pytest.fixture
def app_endpoint(dify_app_endpoint):
    return dify_app_endpoint + "/kaye-commit-sense"
