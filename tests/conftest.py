import pytest

from api import create_app


@pytest.fixture(scope="session")
def flask_app():
    app = create_app()
    app.config["TESTING"] = True
    yield app


@pytest.fixture(scope="session")
def flask_test_client(flask_app):
    return flask_app.test_client()
