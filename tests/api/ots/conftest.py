import pytest


@pytest.fixture(scope="session")
def main0():
    return "# Opus Tag Smith"


@pytest.fixture(scope="session")
def main1():
    return "You are a **media information extraction agent**"


@pytest.fixture(scope="session")
def main2():
    return "- Identify the work and its media type"


@pytest.fixture(scope="session")
def main3():
    return "- Describe the content when useful"


@pytest.fixture(scope="session")
def title0():
    return "## title"


@pytest.fixture(scope="session")
def title1():
    return "Extract the work's **original title**"


@pytest.fixture(scope="session")
def title2():
    return "- Preserve the title in its **original language**"


@pytest.fixture(scope="session")
def title3():
    return "- Recover human-readable title formatting from filenames"


@pytest.fixture(scope="session")
def title4():
    return "hyphens, or other separators"


@pytest.fixture(scope="session")
def year0():
    return "## release year"


@pytest.fixture(scope="session")
def year1():
    return "The year this exact media version"


@pytest.fixture(scope="session")
def year2():
    return "four-digit year format, e.g. `2015`."


@pytest.fixture(scope="session")
def tags0():
    return "## tags"


@pytest.fixture(scope="session")
def tag_instruction1():
    return "Extract **as many tags as possible**"


@pytest.fixture(scope="session")
def tag_instruction2():
    return "- Every tag must be directly grounded"


@pytest.fixture(scope="session")
def tag_instruction3():
    return "- When information is uncertain or partially"


@pytest.fixture(scope="session")
def tag_instruction4():
    return "When the provided data contains information"


@pytest.fixture(scope="session")
def tag_instruction5():
    return "A list of standard tags is provided below as reference"


@pytest.fixture(scope="session")
def tags1():
    return "- `zh[娛樂至死]`: title translation"


@pytest.fixture(scope="session")
def tags2():
    return "- `en[War and Peace]`"
