import pytest


@pytest.fixture(scope="session")
def main0():
    return "# Opus Tag Smith"


@pytest.fixture(scope="session")
def title0():
    return "## Title"


@pytest.fixture(scope="session")
def tags0():
    return "## Tags"
