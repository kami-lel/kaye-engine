import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def cli_command():
    return "python3 -m kaye "


# metadata md filenames  =======================================================


@pytest.fixture(scope="session")
def md_filenames():
    return [
        "style-guide-capitalization",
        "style-guide-briefness-style",
        "style-guide-good-writing",
    ]


@pytest.fixture(scope="session")
def md_filename2skill_name():
    return {
        "style-guide-capitalization": "Style Guide Capitalization",
        "style-guide-briefness-style": "Style Guide Briefness Style",
        "style-guide-good-writing": "Style Guide Good Writing",
    }
