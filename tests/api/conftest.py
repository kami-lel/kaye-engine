import pytest

from kaye.api import create_app


@pytest.fixture(scope="session")
def flask_test_client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture(scope="session")
def dify_app_endpoint():
    return "/kaye/dify-app"
