def assert_edit_changelog0(testee_content):

    return "#### edit CHANGELOG" in testee_content


def assert_edit_changelog1(testee_content):
    return (
        "- edit `CHANGELOG.md` or CHANGELOG-Style File "
        "to reflect the current project state"
        in testee_content
    )


def assert_edit_changelog2(testee_content):
    return (
        "- Follow the **Changelog Writer** rule for format, versioning, "
        "and entry style"
        in testee_content
    )
