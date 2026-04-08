import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def sense_endpoint(app_endpoint):
    return app_endpoint + "/sense"
