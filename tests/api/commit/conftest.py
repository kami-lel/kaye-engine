import pytest


@pytest.fixture
def app_endpoint(dify_app_endpoint):
    return dify_app_endpoint + "/kaye-commit-sense"


@pytest.fixture
def primary_endpoint(app_endpoint):
    return app_endpoint + "/primary-message"
