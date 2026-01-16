import pytest

from api import create_app


@pytest.fixture(scope="session")
def flask_test_client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


HTTP_API_IP = "127.0.0.1"
HTTP_API_PORT = 11255

# TODO implement API unit tests (using sh?)
