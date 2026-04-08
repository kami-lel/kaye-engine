import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def sense_endpoint(app_endpoint):
    return app_endpoint + "/sense"


@pytest.fixture
def request_body():
    return {"pre_sense_role": "", "difficulty_override": 0}
