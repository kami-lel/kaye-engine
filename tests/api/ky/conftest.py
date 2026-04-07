import pytest


@pytest.fixture(scope="session")
def app_endpoint(dify_app_endpoint):
    return dify_app_endpoint + "/ky"


@pytest.fixture(scope="session")
def sense_endpoint(app_endpoint):
    return app_endpoint + "/sense"


@pytest.fixture(scope="session")
def task_endpoint(app_endpoint):
    return app_endpoint + "/task"
