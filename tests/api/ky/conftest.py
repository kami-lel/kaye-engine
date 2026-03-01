import pytest


@pytest.fixture
def app_endpoint(dify_app_endpoint):
    return dify_app_endpoint + "/ky"


@pytest.fixture
def sense_endpoint(app_endpoint):
    return app_endpoint + "/sense"


@pytest.fixture
def task_endpoint(app_endpoint):
    return app_endpoint + "/task"
