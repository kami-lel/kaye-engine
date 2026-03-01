import pytest


@pytest.fixture
def app_endpoint():
    return "/kaye/dify-app/ky"


@pytest.fixture
def sense_endpoint(app_endpoint):
    return app_endpoint + "/sense"


@pytest.fixture
def task_endpoint(app_endpoint):
    return app_endpoint + "/task"
