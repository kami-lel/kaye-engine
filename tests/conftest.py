import pytest

from api import create_app


@pytest.fixture(scope="session")
def flask_test_client():
    app = create_app()
    app.config["TESTING"] = True
    ctx = app.app_context
    ctx.push()
    client = app.test_client()
    yield client
    ctx.pop()
