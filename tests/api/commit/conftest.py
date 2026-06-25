import pytest


@pytest.fixture(scope="session")
def app_endpoint(dify_app_endpoint):
    return dify_app_endpoint + "/kaye-commit-sense"


@pytest.fixture(scope="session")
def primary_endpoint(app_endpoint):
    return app_endpoint + "/primary-message"
