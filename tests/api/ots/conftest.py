import pytest


@pytest.fixture(scope="session")
def ots0():
    return "# Opus Tag Smith"


@pytest.fixture(scope="session")
def ots1():
    return "You are a **media information extraction agent**"


@pytest.fixture(scope="session")
def ots2():
    return "- Identify the work and its media type"


@pytest.fixture(scope="session")
def ots3():
    return "- Extract relevant metadata and technical details"


@pytest.fixture(scope="session")
def title0():
    return "### title & subtitle"


@pytest.fixture(scope="session")
def title1():
    return (
        "Extract the work's **title** and **subtitle** as two separate fields"
    )


@pytest.fixture(scope="session")
def title2():
    return "- **title**: the primary title of the work"


@pytest.fixture(scope="session")
def title3():
    return (
        "- **subtitle**: the secondary title of the work; "
        "can be **empty** if the work has no subtitle"
    )


@pytest.fixture(scope="session")
def title4():
    return (
        "- Preserve the text in its **original language**, "
        "even if the user provides it in another language"
    )


@pytest.fixture(scope="session")
def title5():
    return (
        "- Recover human-readable formatting from "
        "filenames, slugs, broken encoding, or truncated text when possible"
    )


@pytest.fixture(scope="session")
def title6():
    return "- Do not include episode name"


@pytest.fixture(scope="session")
def title7():
    return "> *Dune: Part Two*"


@pytest.fixture(scope="session")
def title8():
    return "- title: Dune"


@pytest.fixture(scope="session")
def title9():
    return "- subtitle: Part Two"


@pytest.fixture(scope="session")
def title10():
    return "> *Inception*"


@pytest.fixture(scope="session")
def title11():
    return "Extract as:"


@pytest.fixture(scope="session")
def title12():
    return "- title: Inception"


@pytest.fixture(scope="session")
def title13():
    return "- subtitle: *(empty)*"


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
def tag_instruction0():
    return "## tags"


@pytest.fixture(scope="session")
def tag_instruction1():
    return "Extract **as many tags as possible**"


@pytest.fixture(scope="session")
def tag_instruction2():
    return "- Every tag must be directly grounded"


@pytest.fixture(scope="session")
def tag_instruction3():
    return "when a specific tag is present"


@pytest.fixture(scope="session")
def tag_instruction4():
    return "When the provided data contains information"


@pytest.fixture(scope="session")
def tag_instruction5():
    return "A list of standard tags is provided below as reference"


@pytest.fixture(scope="session")
def tags_cm1():
    return (
        "- **Translated title**: Include **only** when the translated title"
        " differs from the `title` field."
    )


@pytest.fixture(scope="session")
def tags_cm2():
    return "  - Format: `lang[Translated Title]`"


@pytest.fixture(scope="session")
def tags_cm3():
    return "    - `zh[娛樂至死]` (when title = `Amusing Ourselves to Death`)"


@pytest.fixture(scope="session")
def tags_cm4():
    return "    - `en[The Stranger]` (when title = `L'Étranger`)"
